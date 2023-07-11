import sys
import os
import torch
from typing import Any, Callable, cast, Dict, List, Optional, Tuple
from os.path import basename
import tarfile
import json
import numpy as np
import copy
import bisect
import random

# def has_file_allowed_extension(filename: str, extensions: Tuple[str, ...]) -> bool:
#     """Checks if a file is an allowed extension.
#     Args:
#         filename (string): path to a file
#         extensions (tuple of strings): extensions to consider (lowercase)
#     Returns:
#         bool: True if the filename ends with one of given extensions
#     """
#     return filename.lower().endswith(extensions)


# def find_classes(dir: str) -> Tuple[List[str], Dict[str, int]]:
#         """
#         Finds the class folders in a dataset.
#         Args:
#             dir (string): Root directory path.
#         Returns:
#             tuple: (classes, class_to_idx) where classes are relative to (dir), and class_to_idx is a dictionary.
#         Ensures:
#             No class is a subdirectory of another.
#         """
#         classes = [d.name for d in os.scandir(dir) if d.is_dir()]
#         classes.sort()
#         class_to_idx = {cls_name: i for i, cls_name in enumerate(classes)}
#         return classes, class_to_idx




# def make_dataset(
#     directory: str,
#     class_to_idx: Dict[str, int],
#     extensions: Optional[Tuple[str, ...]] = None,
#     is_valid_file: Optional[Callable[[str], bool]] = None,
# ) -> List[Tuple[str, int]]:
#     """Generates a list of samples of a form (path_to_sample, class).
#     Args:
#         directory (str): root dataset directory
#         class_to_idx (Dict[str, int]): dictionary mapping class name to class index
#         extensions (optional): A list of allowed extensions.
#             Either extensions or is_valid_file should be passed. Defaults to None.
#         is_valid_file (optional): A function that takes path of a file
#             and checks if the file is a valid file
#             (used to check of corrupt files) both extensions and
#             is_valid_file should not be passed. Defaults to None.
#     Raises:
#         ValueError: In case ``extensions`` and ``is_valid_file`` are None or both are not None.
#     Returns:
#         List[Tuple[str, int]]: samples of a form (path_to_sample, class)
#     """
#     instances = []
#     directory = os.path.expanduser(directory)
#     both_none = extensions is None and is_valid_file is None
#     both_something = extensions is not None and is_valid_file is not None
#     if both_none or both_something:
#         raise ValueError("Both extensions and is_valid_file cannot be None or not None at the same time")
#     if extensions is not None:
#         def is_valid_file(x: str) -> bool:
#             return has_file_allowed_extension(x, cast(Tuple[str, ...], extensions))
#     is_valid_file = cast(Callable[[str], bool], is_valid_file)
#     for target_class in sorted(class_to_idx.keys()):
#         class_index = class_to_idx[target_class]
#         target_dir = os.path.join(directory, target_class)
#         if not os.path.isdir(target_dir):
#             continue
#         for root, _, fnames in sorted(os.walk(target_dir, followlinks=True)):
#             for fname in sorted(fnames):
#                 path = os.path.join(root, fname)
#                 if is_valid_file(path):
#                     item = path, target_class
#                     instances.append(item)
#     return instances

def load_categories(ann_file):
    with open(ann_file, 'r') as f:
        annotations = json.load(f)
    categories = annotations['categories']
    category_names = [category['name'] for category in categories]
    category_ids = [category['id'] for category in categories]
    merged_dict = dict(zip(category_names, category_ids))

    return category_names, merged_dict

def _quantize(x, bins):
    bins = copy.deepcopy(bins)
    bins = sorted(bins)
    quantized = list(map(lambda y: bisect.bisect_right(bins, y), x))
    return quantized

def create_aspect_ratio_groups(annotations,group_size, k=3):
    bins = (2 ** np.linspace(-1, 1, 2 * k + 1)).tolist() if k > 0 else [1.0]
    # print("bins ->", bins)
    # Calculate the aspect ratio for each image
    groups = []
    num_groups = len(annotations['images'])//group_size
    for image in annotations['images']:
        width = image['width']
        height = image['height']
        aspect_ratio = width / height
        aspect_ratio_group = _quantize([aspect_ratio], bins)
        image['aspect_ratio_group'] = aspect_ratio_group[0]
        groups.append(aspect_ratio_group[0])
    # print("grouping to bins -> ", groups)
    # ------------------
    # wrapping img id and aspect ratio in a dict
    imgid_aspect_ratio = {image['id']: image['aspect_ratio_group'] for image in annotations['images']}
    # print("imgid_aspect_ratio ->", imgid_aspect_ratio)

    # group it based on aspect ratio in a dict 
    grouped_dict = {}
    for key, value in imgid_aspect_ratio.items():
        if value not in grouped_dict:
            grouped_dict[value] = {}
        grouped_dict[value][key] = value
    
    grouped_dict = {k: v for k, v in sorted(grouped_dict.items())}
    # print("grouped_dict ->", grouped_dict)

    # take img_id as group size in the grouped_dict
    grouped_mytar = {}
    group_num_aspect_ratio = 0
    for key, value in grouped_dict.items():
        # shuffle each grouped aspect ratio
        # print("data value ->", value)
        keys = list(value.keys())
        random.shuffle(keys)
        shuffled_data = {key: value[key] for key in keys}
        # print("shuffled_data ->", shuffled_data)
        
        # make grouped data that contain same as group size
        if len(value) >= group_size:
            num_iter_to_stop = len(value)//group_size
            # print("num_iter_to_stop -> ", num_iter_to_stop)
            values_in_group = 0
            for x in value.copy():
                if num_iter_to_stop>0:
                    if group_num_aspect_ratio not in grouped_mytar:
                        grouped_mytar[group_num_aspect_ratio] = {}
                    grouped_mytar[group_num_aspect_ratio][x] = key
                    del value[x]
                    values_in_group +=1
                    if values_in_group == group_size :
                        values_in_group = 0
                        num_iter_to_stop -= 1
                        group_num_aspect_ratio += 1

    print("rest of grouped_dict that cant be grouping ->", grouped_dict)
    print("grouped_mytar -> ", grouped_mytar)
    grouped_mytar = {k: list(v) for k, v in grouped_mytar.items()}
    print("grouped_mytar -> ", grouped_mytar)
    grouped_dict = dict(sorted(grouped_dict.items(), key=lambda item: len(item[1]), reverse=True))

    for key, value in grouped_dict.items():
        print(key, value)
        if len(grouped_mytar)<num_groups:
            for x in value:
                if group_num_aspect_ratio not in grouped_mytar:
                    grouped_mytar[group_num_aspect_ratio] = []
                grouped_mytar[group_num_aspect_ratio].append(x)
            
            print("->",len(grouped_mytar[group_num_aspect_ratio]))

            while len(grouped_mytar[group_num_aspect_ratio]) < group_size:
                for image in annotations['images']:
                    if image['aspect_ratio_group'] == key:
                        found_id = image['id']
                        print("found_id -> ", found_id)
                        break
                grouped_mytar[group_num_aspect_ratio].append(found_id)
                print("len ->", len(grouped_mytar[group_num_aspect_ratio]))
                print(grouped_mytar)

            group_num_aspect_ratio += 1
            
                

    # values_in_group = 0
    # for key, value in grouped_dict.items():
    #     for x in value:
    #         if group_num_aspect_ratio not in grouped_mytar:
    #             grouped_mytar[group_num_aspect_ratio] = {}
    #         grouped_mytar[group_num_aspect_ratio][x] = key
    #         values_in_group += 1
    #         if values_in_group == group_size :
    #             values_in_group = 0
    #             # num_iter_to_stop -= 1
    #             group_num_aspect_ratio += 1

    print("sort rest of grouped_dict that cant be grouping->", grouped_dict)
    print("final grouped_mytar -> ", grouped_mytar, len(grouped_mytar))
    quit()
    list_imgid_sorted_by_aspect_ratio = []
    for key, value in grouped_mytar.items():
        for x in value:
            list_imgid_sorted_by_aspect_ratio.append(x)
    # print("list_imgid_sorted_by_aspect_ratio -> ", list_imgid_sorted_by_aspect_ratio)

    # change the order img id based on grouping aspect ratio
    annotations['images'] = sorted(annotations['images'], key=lambda d: list_imgid_sorted_by_aspect_ratio.index(d['id']))   
    # for value in annotations['images']:
    #     print(value)
    # -------------------
    # Sort the images based on aspect ratio
    # annotations['images'] = sorted(annotations['images'], key=lambda x: x['aspect_ratio_group'])
    # print("annotations['images'] -> ", annotations['images'] )
    return annotations

def get_samples_from_annotations(ann_file, images_folder, group_size):
    with open(ann_file, 'r') as f:
        annotations = json.load(f)

    categories = annotations['categories']
    category_mapping = {category['id']: category['name'] for category in categories}
    
    annotations = create_aspect_ratio_groups(annotations,group_size, k=3)
    # print("annotations -> ", annotations)

    samples = []
    for image in annotations['images']:
        list_annotation = []
        image_id = image['id']
        aspect_ratio_group = image['aspect_ratio_group']
        # print("aspect_ratio_group -> ", aspect_ratio_group)
        image_path = images_folder + image['file_name']  # Replace with the actual path to the images
        for annotation in annotations['annotations']:
            image_annotation = []
            if annotation['image_id'] == image_id:
                # category_id = annotation['category_id']
                # bbox = annotation['bbox']
                # area = annotation['area']
                # iscrowd = annotation['iscrowd']
                
                # image_annotation.extend([image_id, category_id, bbox, area, iscrowd])
                list_annotation.append(annotation)
            
            #print("list_annotation -> ", list_annotation)

        samples.append((image_id, aspect_ratio_group, image_path, list_annotation))    
        # print("aspect_ratio_group -> ", aspect_ratio_group)
    return samples

#-------------------

# def _compute_aspect_ratios_coco_dataset(img_height, img_width, indices=None):
#     # print("len(dataset) -> ", len(dataset))
#     # print(dataset[0])
#     # if indices is None:
#     #     indices = range(len(dataset))
#     # aspect_ratios = []
#     # for i in indices:
#     #     print(i, indices)
#     #     img_info = dataset.coco.imgs[dataset.ids[i]]
#     #     print("img_info -> ", img_info)
#     #     aspect_ratio = float(img_info["width"]) / float(img_info["height"])
#     #     aspect_ratios.append(aspect_ratio)

#     img_info = dataset.coco.imgs[dataset.ids[i]]
#     print("img_info -> ", img_info)
#     aspect_ratio = float(img_width) / float(img_height)

#     return aspect_ratios


# def _quantize(x, bins):
#     bins = copy.deepcopy(bins)
#     bins = sorted(bins)
#     quantized = list(map(lambda y: bisect.bisect_right(bins, y), x))
#     return quantized

# def create_aspect_ratio_groups(img_height, img_width, k=0):
#     # print("dataset -> ", dataset)
#     aspect_ratios = _compute_aspect_ratios_coco_dataset(img_height, img_width)
#     print("aspect_ratio", aspect_ratios)
#     #print("np.linspace(-1, 1, 2 * k + 1) ->", np.linspace(-1, 1, 2 * k + 1))
#     bins = (2 ** np.linspace(-1, 1, 2 * k + 1)).tolist() if k > 0 else [1.0]
#     print("bins ->", bins)
#     quit()
#     groups = _quantize(aspect_ratios, bins)
#     # count number of elements per group
#     counts = np.unique(groups, return_counts=True)[1]
#     fbins = [0] + bins + [np.inf]
#     print("Using {} as bins for aspect ratio quantization".format(fbins))
#     print("Count of instances per bin: {}".format(counts))
#     #print("sum ->", sum(counts))
#     #print("Stop")
#     print("groups aspect ratio -> ", groups)
#     #quit()
#     return groups



IMG_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.ppm', '.bmp', '.pgm', '.tif',
                  '.tiff', '.webp', '.pickle', '.zip', 'tar', 'mytar')


if len(sys.argv) < 4:
    print('python group-needle-detection.py <train_folder> <groupsize> <mytar_save_folder>')
    print('example: python group-needle-detection-based-images-annotations.py ~/mini-coco-dataset/coco_minitrain_25k 4 ~/mini-coco-dataset/grouped-data-images-annotations')
    exit()

train_folder = sys.argv[1]
print(train_folder)
group_size = int(sys.argv[2])
print(group_size)
mytar_save_folder = sys.argv[3] + '/{}/'.format(group_size)
print(mytar_save_folder)

os.makedirs(mytar_save_folder, exist_ok=True)

ann_train_file = train_folder + "/annotations/instances_train2017.json"
ann_val_file = train_folder + "/annotations/instances_val2017.json"

# Load category names from COCO annotations
classes, class_to_idx= load_categories(ann_train_file)
print(len(classes), len(class_to_idx))

# classes, class_to_idx = find_classes(train_folder)
# print(classes, class_to_idx)
# print("classes: \n {} \n class_to_idx: \n {}".format(classes, class_to_idx))

# instances = make_dataset(images_folder, class_to_idx, IMG_EXTENSIONS, None)

images_folder = train_folder + "/images/train2017/"
instances = get_samples_from_annotations(ann_train_file, images_folder, group_size)
print("number of images: {}".format(len(instances)))
# print(instances)

generator = torch.Generator()

# with open('perms/seed1.txt') as f:
#     seed = int(f.read())
#     f.close() j, class_id, offset, img_size, image_path, 

# generator.manual_seed(100)
# permutation = torch.randperm(len(instances), generator=generator).tolist()

# it = iter(permutation)
# print("len(permutation) ->", len(permutation) )
group_num = int(len(instances) / group_size)



with open(mytar_save_folder + "metadata.txt", 'w') as metadata_writer:
    metadata_writer.write('{}\n'.format(len(classes)))
    for class_name in classes:
        metadata_writer.write('{}\n'.format(class_name))

    metadata = ''
    idx = 0
    for i in range(group_num):
        mytar_name = 'filegroup-{}.mytar'.format(i)
        imgdata = b''
        offset = 0
        metadata += '{},{}\n'.format(mytar_name,group_size)
        for j in range(group_size):
            image_id, aspect_ratio_group, img_path, list_annotation = instances[idx]
            idx += 1
            img_size = os.path.getsize(img_path)

            # aspect_ratio_group = create_aspect_ratio_groups(img_height, img_width, k=3)
            
            # print("stop")
            # quit()
            
            metadata += '{},{},{},{},{}-{}\n'.format(j, image_id, aspect_ratio_group, offset, img_size, list_annotation)
            offset += img_size
            with open(img_path, 'rb') as reader:
                img = reader.read()
                imgdata += img
        with open(mytar_save_folder + mytar_name, 'wb') as writer:
            writer.write(imgdata)


    metadata_writer.write(metadata)


print("group_size: {} group num: {}".format(
           group_size, group_num))