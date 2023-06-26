import sys
import os
import torch
from typing import Any, Callable, cast, Dict, List, Optional, Tuple
from os.path import basename
import tarfile
import json

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

def get_samples_from_annotations(ann_file, images_folder):
    with open(ann_file, 'r') as f:
        annotations = json.load(f)

    categories = annotations['categories']
    category_mapping = {category['id']: category['name'] for category in categories}
    
    samples = []
    for image in annotations['images']:
        image_id = image['id']
        image_path = images_folder + image['file_name']  # Replace with the actual path to the images
        for annotation in annotations['annotations']:
            if annotation['image_id'] == image_id:
                class_id = annotation['category_id']
                class_name = category_mapping[class_id]
                samples.append((image_path, class_name))
                break
    
    return samples



IMG_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.ppm', '.bmp', '.pgm', '.tif',
                  '.tiff', '.webp', '.pickle', '.zip', 'tar', 'mytar')


if len(sys.argv) < 4:
    print('python group-needle-detection.py <train_folder> <groupsize> <mytar_save_folder>')
    print('example: python group-needle-detection.py ~/mini-coco-dataset/coco_minitrain_25k 4 ~/mini-coco-dataset/grouped-data')
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
print("classes: \n {} \n class_to_idx: \n {}".format(classes, class_to_idx))

# instances = make_dataset(images_folder, class_to_idx, IMG_EXTENSIONS, None)

images_folder = train_folder + "/images/train2017/"
instances = get_samples_from_annotations(ann_train_file, images_folder)
print("number of images: {}".format(len(instances)))
print(instances)

generator = torch.Generator()

# with open('perms/seed1.txt') as f:
#     seed = int(f.read())
#     f.close()

generator.manual_seed(100)
permutation = torch.randperm(len(instances), generator=generator).tolist()

it = iter(permutation)
group_num = int(len(permutation) / group_size)



with open(mytar_save_folder + "metadata.txt", 'w') as metadata_writer:
    metadata_writer.write('{}\n'.format(len(classes)))
    for class_name in classes:
        metadata_writer.write('{}\n'.format(class_name))

    metadata = ''
    for i in range(group_num):
        mytar_name = 'filegroup-{}.mytar'.format(i)
        imgdata = b''
        offset = 0
        metadata += '{},{}\n'.format(mytar_name,group_size)
        for j in range(group_size):
            idx = permutation[i*group_size + j]
            img_path, target_class = instances[idx]
            img_size = os.path.getsize(img_path)
            
            # print("stop")
            # quit()
            
            metadata += '{},{},{},{},{}\n'.format(j, target_class, offset, img_size,img_path)
            offset += img_size
            with open(img_path, 'rb') as reader:
                img = reader.read()
                imgdata += img
        with open(mytar_save_folder + mytar_name, 'wb') as writer:
            writer.write(imgdata)


    metadata_writer.write(metadata)


print("group_size: {} group num: {}".format(
           group_size, group_num))