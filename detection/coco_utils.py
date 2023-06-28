import copy
import os
from PIL import Image

import torch
import torch.utils.data
import torchvision

from pycocotools import mask as coco_mask
from pycocotools.coco import COCO

import transforms as T
import json
import io


class FilterAndRemapCocoCategories(object):
    def __init__(self, categories, remap=True):
        self.categories = categories
        self.remap = remap

    def __call__(self, image, target):
        anno = target["annotations"]
        anno = [obj for obj in anno if obj["category_id"] in self.categories]
        if not self.remap:
            target["annotations"] = anno
            return image, target
        anno = copy.deepcopy(anno)
        for obj in anno:
            obj["category_id"] = self.categories.index(obj["category_id"])
        target["annotations"] = anno
        return image, target


def convert_coco_poly_to_mask(segmentations, height, width):
    masks = []
    for polygons in segmentations:
        rles = coco_mask.frPyObjects(polygons, height, width)
        mask = coco_mask.decode(rles)
        if len(mask.shape) < 3:
            mask = mask[..., None]
        mask = torch.as_tensor(mask, dtype=torch.uint8)
        mask = mask.any(dim=2)
        masks.append(mask)
    if masks:
        masks = torch.stack(masks, dim=0)
    else:
        masks = torch.zeros((0, height, width), dtype=torch.uint8)
    return masks


class ConvertCocoPolysToMask(object):
    def __call__(self, image, target):
        print("image, target (conpolys)-> ", image, target)
        print("image_id1 -> ", target["image_id"])
        w, h = image.size

        image_id = target["image_id"]
        print("image_id2 -> ", image_id)
        image_id = torch.tensor([image_id])

        print("target -> ", target.keys())
        anno = target["annotations"]
        print("anno -> ", anno)
        for obj in anno:
            print("obj -> ", obj)
            print("obj['iscrowd'] -> ", obj['iscrowd'])
            if obj['iscrowd'] == 0:
                print('icrowd == 0 ....')

        anno = [obj for obj in anno if obj['iscrowd'] == 0]

        boxes = [obj["bbox"] for obj in anno]
        # guard against no boxes via resizing
        boxes = torch.as_tensor(boxes, dtype=torch.float32).reshape(-1, 4)
        boxes[:, 2:] += boxes[:, :2]
        boxes[:, 0::2].clamp_(min=0, max=w)
        boxes[:, 1::2].clamp_(min=0, max=h)

        classes = [obj["category_id"] for obj in anno]
        classes = torch.tensor(classes, dtype=torch.int64)

        segmentations = [obj["segmentation"] for obj in anno]
        masks = convert_coco_poly_to_mask(segmentations, h, w)

        keypoints = None
        if anno and "keypoints" in anno[0]:
            keypoints = [obj["keypoints"] for obj in anno]
            keypoints = torch.as_tensor(keypoints, dtype=torch.float32)
            num_keypoints = keypoints.shape[0]
            if num_keypoints:
                keypoints = keypoints.view(num_keypoints, -1, 3)

        keep = (boxes[:, 3] > boxes[:, 1]) & (boxes[:, 2] > boxes[:, 0])
        boxes = boxes[keep]
        classes = classes[keep]
        masks = masks[keep]
        if keypoints is not None:
            keypoints = keypoints[keep]

        target = {}
        target["boxes"] = boxes
        target["labels"] = classes
        target["masks"] = masks
        target["image_id"] = image_id
        if keypoints is not None:
            target["keypoints"] = keypoints

        # for conversion to coco api
        area = torch.tensor([obj["area"] for obj in anno])
        iscrowd = torch.tensor([obj["iscrowd"] for obj in anno])
        target["area"] = area
        target["iscrowd"] = iscrowd

        return image, target


def _coco_remove_images_without_annotations(dataset, cat_list=None):
    def _has_only_empty_bbox(anno):
        # print("anno", anno)
        # for obj in anno:
        #     for o in obj["bbox"][2:]:
        #         print('o -->', o)
        #         print(o<=1)
        #         print(any(o<=1))
        #         print(all(any(o<=1)))
        #         quit()
        return all(any(o <= 1 for o in obj["bbox"][2:]) for obj in anno)

    def _count_visible_keypoints(anno):
        # print("anno", anno)
        # for ann in anno:
        #     for v in ann["keypoints"][2::3]:
        #         if v > 0:
        #             print('v -->', v)
        #         break
        return sum(sum(1 for v in ann["keypoints"][2::3] if v > 0) for ann in anno)

    min_keypoints_per_image = 10

    def _has_valid_annotation(anno):
        # if it's empty, there is no annotation
        if len(anno) == 0:
            return False
        # if all boxes have close to zero area, there is no annotation
        if _has_only_empty_bbox(anno):
            return False
        # keypoints task have a slight different critera for considering
        # if an annotation is valid
        if "keypoints" not in anno[0]:
            return True
        # for keypoint detection tasks, only consider valid images those
        # containing at least min_keypoints_per_image
        if _count_visible_keypoints(anno) >= min_keypoints_per_image:
            return True
        return False

    assert isinstance(dataset, torchvision.datasets.CocoDetection)
    ids = []
    print("dataset.ids -> ", dataset.ids)
    for ds_idx, img_id in enumerate(dataset.ids):
        ann_ids = dataset.coco.getAnnIds(imgIds=img_id, iscrowd=None)
        anno = dataset.coco.loadAnns(ann_ids)
        if cat_list:
            anno = [obj for obj in anno if obj["category_id"] in cat_list]
        if _has_valid_annotation(anno):
            ids.append(ds_idx)

    dataset = torch.utils.data.Subset(dataset, ids)
    return dataset


def convert_to_coco_api(ds):
    coco_ds = COCO()
    # annotation IDs need to start at 1, not 0, see torchvision issue #1530
    ann_id = 1
    dataset = {'images': [], 'categories': [], 'annotations': []}
    categories = set()
    for img_idx in range(len(ds)):
        # find better way to get target
        # targets = ds.get_annotations(img_idx)
        img, targets = ds[img_idx]
        image_id = targets["image_id"].item()
        img_dict = {}
        img_dict['id'] = image_id
        img_dict['height'] = img.shape[-2]
        img_dict['width'] = img.shape[-1]
        dataset['images'].append(img_dict)
        bboxes = targets["boxes"]
        bboxes[:, 2:] -= bboxes[:, :2]
        bboxes = bboxes.tolist()
        labels = targets['labels'].tolist()
        areas = targets['area'].tolist()
        iscrowd = targets['iscrowd'].tolist()
        if 'masks' in targets:
            masks = targets['masks']
            # make masks Fortran contiguous for coco_mask
            masks = masks.permute(0, 2, 1).contiguous().permute(0, 2, 1)
        if 'keypoints' in targets:
            keypoints = targets['keypoints']
            keypoints = keypoints.reshape(keypoints.shape[0], -1).tolist()
        num_objs = len(bboxes)
        for i in range(num_objs):
            ann = {}
            ann['image_id'] = image_id
            ann['bbox'] = bboxes[i]
            ann['category_id'] = labels[i]
            categories.add(labels[i])
            ann['area'] = areas[i]
            ann['iscrowd'] = iscrowd[i]
            ann['id'] = ann_id
            if 'masks' in targets:
                ann["segmentation"] = coco_mask.encode(masks[i].numpy())
            if 'keypoints' in targets:
                ann['keypoints'] = keypoints[i]
                ann['num_keypoints'] = sum(k != 0 for k in keypoints[i][2::3])
            dataset['annotations'].append(ann)
            ann_id += 1
    dataset['categories'] = [{'id': i} for i in sorted(categories)]
    coco_ds.dataset = dataset
    coco_ds.createIndex()
    return coco_ds


def get_coco_api_from_dataset(dataset):
    for _ in range(10):
        if isinstance(dataset, torchvision.datasets.CocoDetection):
            break
        if isinstance(dataset, torch.utils.data.Subset):
            dataset = dataset.dataset
    if isinstance(dataset, torchvision.datasets.CocoDetection):
        return dataset.coco
    return convert_to_coco_api(dataset)

def mytar_loader(path: str, group_metadata):
    imgs = []
    targets = []
    print("path -> ", path)
    with open(path, 'rb') as f:
        f = f.read()
        for img_info in group_metadata:
            img_start = img_info['start']
            img_end = img_start + img_info['img_size']
            annotations = img_info['annotations']
            # img_class_idx = img_info['img_class_idx']
            # print('img_class_idx:{}'.format(img_class_idx))
            img_data = f[img_start:img_end]
            iobytes = io.BytesIO(img_data)
            img = Image.open(iobytes)
            imgs.append(img.convert('RGB'))
            targets.append(annotations)
    return imgs, targets

def mytar_img_id_annotations(path: str, group_metadata, _transforms):
    print("mytar_img_id_annotations...")
    imgs = []
    targets = []
    print("path -> ", path)
    with open(path, 'rb') as f:
        f = f.read()
        for img_info in group_metadata:
            img_id = img_info['img_id']
            img_start = img_info['start']
            img_end = img_start + img_info['img_size']
            annotations = img_info['annotations']
            # img_class_idx = img_info['img_class_idx']
            # print('img_class_idx:{}'.format(img_class_idx))
            img_data = f[img_start:img_end]
            iobytes = io.BytesIO(img_data)
            img = Image.open(iobytes)
            img = img.convert('RGB')

            # print("sadasd")
            # target = dict(image_id=img_id, annotations=annotations)
            target = annotations
            if _transforms is not None:
                print("self.transforms -> ", _transforms)
                print("transforming..")
                img, target = _transforms(img, target)

            imgs.append(img)
            targets.append(target)

    return imgs, targets


# meng: get metadata so we know the classes and index of images.
def get_metadata_mytar(
    directory: str,
    group_size: int
):
    directory = os.path.expanduser(directory)
    metadata_path = os.path.join(directory, str(2)+ "/metadata.txt")
    metadata = []
    classes = []
    with open(metadata_path, 'r') as reader:
        # first get all classes
        class_count = int(reader.readline().strip())
        for _ in range(class_count):
            class_name = reader.readline().strip()
            classes.append(class_name)
        classes.sort()
        class_to_idx = {cls_name: i for i, cls_name in enumerate(classes)}
        # print(class_to_idx)
        # then get all groups metadata
        while reader:
            groupname = reader.readline().strip().split(',')[0]
            if(groupname == ''):
                break
            group = []
            for i in range(group_size):
                # print("reader -> ", reader.readline())
                tar_info, img_anns = reader.readline().strip().split('-')
                values = tar_info.strip().split(',')
                # print("values -> ", values)
                # quit()
                idx = int(values[0])
                img_id = int(values[1])
                start = int(values[2])
                img_size = int(values[3])
                # annotations = str(values[4])
                # print("annotations -> ", annotations)
                # annotations = str(values[5])
                # print("annotations -> ", annotations)
                # annotations = reader.readline().strip().split('-')[3]
                # print(type(img_anns))
                
                # print("annotations -> ", img_anns)
                

                string_data = img_anns.replace("'", "\"")
                # print(type(string_data))
                

                annotations = json.loads(string_data)
                data_dict = {'image_id': img_id, 'annotations': annotations}
                print("data_dict -> ", data_dict)
                # quit()
                # print("annotations (in coco_utils) -> ",type(annotations), annotations)
                # print("index 0 -> ", annotations[0])
                # print("index 0 0 -> ", type(annotations[0]['image_id']), annotations[0]['image_id'])
                
                group.append({'idx':idx, 'img_id':img_id, 'start':start, 'img_size':img_size, 'annotations': data_dict})
            metadata.append({'groupname':groupname, 'metadata':group})
    # print(class_to_idx)
    # print(metadata)
    return metadata


class CocoDetection(torchvision.datasets.CocoDetection):
    def __init__(self, root, img_folder, ann_file, transforms, is_mytar):
        super(CocoDetection, self).__init__(root, img_folder, ann_file, is_mytar)
        self.is_mytar = is_mytar
        self._transforms = transforms
        if(is_mytar):
            print("grouping using my own tar format!")
        if hasattr(self, 'is_mytar') and self.is_mytar:
            print("Using Mytar...")
            self.metadata = metadata = get_metadata_mytar(root, 2)

    def __getitem__(self, idx):
        print("coco_utils -> ", self.is_mytar)
        if self.is_mytar:
            print("using mytar func from coco_utils.py...")
            # metadata = get_metadata_mytar(root, 4)
            path = self.root + str(2) + '/' + self.metadata[idx]['groupname']
            group_metadata = self.metadata[idx]['metadata']
            samples, targets = mytar_img_id_annotations(path, group_metadata, self._transforms)
            # samples, targets = mytar_loader(path, group_metadata)
            # print("self.transforms -> ", self.transforms)
            # if self._transforms is not None:
            #     samples, targets = self._transforms(samples, targets)

            return samples, targets

        img, target = super(CocoDetection, self).__getitem__(idx)
        # print("img, target=", img, target)
        # quit()
        image_id = self.ids[idx]
        print("image_id=image_id, annotations=target -> ", type(image_id), image_id, type(target), target)

        target = dict(image_id=image_id, annotations=target)
        # print("target -> ", target)

        if self._transforms is not None:
            print("self.transforms -> ", self._transforms)
            print("transforming..")
            img, target = self._transforms(img, target)
        return img, target

    def __len__(self) -> int:
        if self.is_mytar:
            print("self.metada (in len) -> ", len(self.metadata), self.metadata)
            # quit()
            return len(self.metadata)
        else:
            print("self.ids (in len1) -> ", len(self.ids), self.ids)
            return len(self.ids)


def get_coco(root, image_set, transforms, is_mytar, mode='instances'):
    anno_file_template = "{}_{}2017.json"
    PATHS = {
        "train": ("images/train2017", os.path.join("annotations", anno_file_template.format(mode, "train"))),
        "val": ("images/val2017", os.path.join("annotations", anno_file_template.format(mode, "val"))),
        # "train": ("val2017", os.path.join("annotations", anno_file_template.format(mode, "val")))
    }

    t = [ConvertCocoPolysToMask()]

    if transforms is not None:
        t.append(transforms)
    transforms = T.Compose(t)
    # print("TESTING")
    # print("->", image_set)
    img_folder, ann_file = PATHS[image_set]
    print("img_folder, ann_file- >", img_folder, ann_file)
    # print("->", img_folder, ann_file)
    img_folder = os.path.join(root, img_folder)
    ann_file = os.path.join(root, ann_file)
    print("img_folder, ann_file- >", img_folder, ann_file)
    # print("->", img_folder, ann_file)
    
    if image_set == "train" and is_mytar:
        print("tar")
        dataset = CocoDetection(root, img_folder, ann_file, transforms=transforms, is_mytar=True)
    else:
        print("val")
        dataset = CocoDetection(root ,img_folder, ann_file, transforms=transforms, is_mytar=False)
    # print('dataset=', dataset)
    # if image_set == "train":
    #     print("enter remove annotaions...")
    #     dataset = _coco_remove_images_without_annotations(dataset)
    # if image_set == "train":
    #     dataset = _coco_remove_images_without_annotations(dataset)

    # dataset = torch.utils.data.Subset(dataset, [i for i in range(500)])
    return dataset


def get_coco_kp(root, image_set, transforms):
    return get_coco(root, image_set, transforms, mode="person_keypoints")
