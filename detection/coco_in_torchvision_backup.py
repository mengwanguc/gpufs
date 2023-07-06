from .vision import VisionDataset
from PIL import Image
import os
import os.path
from typing import Any, Callable, Optional, Tuple

import io
import json

class CocoCaptions(VisionDataset):
    """`MS Coco Captions <https://cocod ataset.org/#captions-2015>`_ Dataset.

    Args:
        root (string): Root directory where images are downloaded to.
        annFile (string): Path to json annotation file.
        transform (callable, optional): A function/transform that  takes in an PIL image
            and returns a transformed version. E.g, ``transforms.ToTensor``
        target_transform (callable, optional): A function/transform that takes in the
            target and transforms it.
        transforms (callable, optional): A function/transform that takes input sample and its target as entry
            and returns a transformed version.

    Example:

        .. code:: python

            import torchvision.datasets as dset
            import torchvision.transforms as transforms
            cap = dset.CocoCaptions(root = 'dir where images are',
                                    annFile = 'json annotation file',
                                    transform=transforms.ToTensor())

            print('Number of samples: ', len(cap))
            img, target = cap[3] # load 4th sample

            print("Image Size: ", img.size())
            print(target)

        Output: ::

            Number of samples: 82783
            Image Size: (3L, 427L, 640L)
            [u'A plane emitting smoke stream flying over a mountain.',
            u'A plane darts across a bright blue sky behind a mountain covered in snow',
            u'A plane leaves a contrail above the snowy mountain top.',
            u'A mountain that has a plane flying overheard in the distance.',
            u'A mountain view with a plume of smoke in the background']

    """

    def __init__(
            self,
            root: str,
            annFile: str,
            transform: Optional[Callable] = None,
            target_transform: Optional[Callable] = None,
            transforms: Optional[Callable] = None,
    ) -> None:
        super(CocoCaptions, self).__init__(root, transforms, transform, target_transform)
        from pycocotools.coco import COCO
        self.coco = COCO(annFile)
        self.ids = list(sorted(self.coco.imgs.keys()))

    def __getitem__(self, index: int) -> Tuple[Any, Any]:
        """
        Args:
            index (int): Index

        Returns:
            tuple: Tuple (image, target). target is a list of captions for the image.
        """
        coco = self.coco
        img_id = self.ids[index]
        ann_ids = coco.getAnnIds(imgIds=img_id)
        anns = coco.loadAnns(ann_ids)
        target = [ann['caption'] for ann in anns]

        path = coco.loadImgs(img_id)[0]['file_name']

        img = Image.open(os.path.join(self.root, path)).convert('RGB')

        if self.transforms is not None:
            img, target = self.transforms(img, target)

        return img, target

    def __len__(self) -> int:
        return len(self.ids)

def mytar_loader(path: str, group_metadata):
    imgs = []
    targets = []
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


# meng: get metadata so we know the classes and index of images.
def get_metadata_mytar(
    directory: str,
    group_size: int
):
    directory = os.path.expanduser(directory)
    # print("dir -> ", directory)
    metadata_path = os.path.join(directory+"/4/metadata.txt")
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
                idx = values[0]
                # img_class = values[1]
                start = int(values[1])
                img_size = int(values[2])
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
                # print(annotations, type(annotations))
                # print(test[0], type(test[0]))
        
                
                # Convert the string to a dictionary
                # annotations = json.loads(annotations)
                # print("annotations -> ", annotations, type(annotations))
                # print("keys -> ", annotations.keys())
                # print("\n")
                # print("annotations -> ", annotations['id' == 1403624])

                




                # Remove the single quotes around the keys and values
                # data_string = annotations.replace("'", '"')
                # print("data_string -> ", data_string)

                # # Parse the string as a list of dictionaries
                # annotations = json.loads(data_string)

                # print("annotations -> ", annotations, type(annotations))
                # img_class_idx = class_to_idx[img_class]
                group.append({'idx':idx, 'start':start, 'img_size':img_size, 'annotations': annotations})
            metadata.append({'groupname':groupname, 'metadata':group})
    # print(class_to_idx)
    # print(metadata)
    return metadata

class CocoDetection(VisionDataset):
    """`MS Coco Detection <https://cocodataset.org/#detection-2016>`_ Dataset.

    Args:
        root (string): Root directory where images are downloaded to.
        annFile (string): Path to json annotation file.
        transform (callable, optional): A function/transform that  takes in an PIL image
            and returns a transformed version. E.g, ``transforms.ToTensor``
        target_transform (callable, optional): A function/transform that takes in the
            target and transforms it.
        transforms (callable, optional): A function/transform that takes input sample and its target as entry
            and returns a transformed version.
    """

    def __init__(
            self,
            root: str,
            img_folder: str,
            annFile: str,
            is_mytar: bool,
            transform: Optional[Callable] = None,
            target_transform: Optional[Callable] = None,
            transforms: Optional[Callable] = None,
    ) -> None:
        super(CocoDetection, self).__init__(root, transforms, transform, target_transform)
        from pycocotools.coco import COCO

        self.is_mytar = is_mytar
        self.img_folder = img_folder
        print("is_mytar -> ", self.is_mytar)
        if hasattr(self, 'is_mytar') and self.is_mytar:
            print("Using Mytar in coco.py...")
            self.metadata = metadata = get_metadata_mytar(root, 4)
        else:
            print('using original init coco.py ...')
            self.coco = COCO(annFile)
            # print("self.coco -> ", self.coco)
            self.ids = list(sorted(self.coco.imgs.keys()))
            # print("self.ids -> ", self.ids)

        

    def __getitem__(self, index: int) -> Tuple[Any, Any]:
        """
        Args:
            index (int): Index

        Returns:
            tuple: Tuple (image, target). target is the object returned by ``coco.loadAnns``.
        """

        # if self.is_mytar:
        #     print("using mytar func from coco.py...")
        #     # metadata = get_metadata_mytar(root, 4)
        #     path = self.root + '/' + str(2) + '/' + self.metadata[index]['groupname']
        #     group_metadata = self.metadata[index]['metadata']
        #     samples, targets = mytar_loader(path, group_metadata)
        #     print("self.transforms -> ", self.transforms)
        #     if self.transforms is not None:
        #         print("transform mytar..")
        #         samples, targets = self.transforms(samples, targets)

        #     return samples, targets

        print("using original func from coco1.py...")
        coco = self.coco
        # print("coco -> ", coco)
        img_id = self.ids[index]
        # print("img_id -> ", img_id)
        ann_ids = coco.getAnnIds(imgIds=img_id)
        # print("ann_ids -> ", ann_ids)
        target = coco.loadAnns(ann_ids)
        # print("target -> ", target)

        path = coco.loadImgs(img_id)[0]['file_name']

        print(self.root)
        print(self.img_folder)
        img = Image.open(os.path.join(self.img_folder, path)).convert('RGB')

        # print("img, target ->", img, target, type(img), type(target))
        
        if self.transforms is not None:
            # print("self.transforms -> ", self.transforms)
            # print("transforming..")
            img, target = self.transforms(img, target)

        return img, target

    # def __len__(self) -> int:
    #     if self.is_mytar:
    #         print("self.metada (in len) -> ", len(self.metadata), self.metadata)
    #         # quit()
    #         return len(self.metadata)
    #     else:
    #         print("self.ids (in len) -> ", len(self.ids), self.ids)
    #         return len(self.ids)
