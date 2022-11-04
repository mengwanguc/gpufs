import sys
import os
import torch
from typing import Any, Callable, cast, Dict, List, Optional, Tuple
from os.path import basename
import tarfile
import zlib
from PIL import Image
import io


def has_file_allowed_extension(filename: str, extensions: Tuple[str, ...]) -> bool:
    """Checks if a file is an allowed extension.
    Args:
        filename (string): path to a file
        extensions (tuple of strings): extensions to consider (lowercase)
    Returns:
        bool: True if the filename ends with one of given extensions
    """
    return filename.lower().endswith(extensions)


def find_classes(dir: str) -> Tuple[List[str], Dict[str, int]]:
        """
        Finds the class folders in a dataset.
        Args:
            dir (string): Root directory path.
        Returns:
            tuple: (classes, class_to_idx) where classes are relative to (dir), and class_to_idx is a dictionary.
        Ensures:
            No class is a subdirectory of another.
        """
        classes = [d.name for d in os.scandir(dir) if d.is_dir()]
        classes.sort()
        class_to_idx = {cls_name: i for i, cls_name in enumerate(classes)}
        return classes, class_to_idx




def make_dataset(
    directory: str,
    class_to_idx: Dict[str, int],
    extensions: Optional[Tuple[str, ...]] = None,
    is_valid_file: Optional[Callable[[str], bool]] = None,
) -> List[Tuple[str, int]]:
    """Generates a list of samples of a form (path_to_sample, class).
    Args:
        directory (str): root dataset directory
        class_to_idx (Dict[str, int]): dictionary mapping class name to class index
        extensions (optional): A list of allowed extensions.
            Either extensions or is_valid_file should be passed. Defaults to None.
        is_valid_file (optional): A function that takes path of a file
            and checks if the file is a valid file
            (used to check of corrupt files) both extensions and
            is_valid_file should not be passed. Defaults to None.
    Raises:
        ValueError: In case ``extensions`` and ``is_valid_file`` are None or both are not None.
    Returns:
        List[Tuple[str, int]]: samples of a form (path_to_sample, class)
    """
    instances = []
    directory = os.path.expanduser(directory)
    both_none = extensions is None and is_valid_file is None
    both_something = extensions is not None and is_valid_file is not None
    if both_none or both_something:
        raise ValueError("Both extensions and is_valid_file cannot be None or not None at the same time")
    if extensions is not None:
        def is_valid_file(x: str) -> bool:
            return has_file_allowed_extension(x, cast(Tuple[str, ...], extensions))
    is_valid_file = cast(Callable[[str], bool], is_valid_file)
    for target_class in sorted(class_to_idx.keys()):
        target_dir = os.path.join(directory, target_class)
        if not os.path.isdir(target_dir):
            continue
        for root, _, fnames in sorted(os.walk(target_dir, followlinks=True)):
            for fname in sorted(fnames):
                subpath = os.path.join(target_class, fname)
                path = os.path.join(directory, subpath)
                if is_valid_file(path):
                    instances.append(subpath)
    return instances





IMG_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.ppm', '.bmp', '.pgm', '.tif',
                  '.tiff', '.webp', '.pickle', '.zip', 'tar', 'mytar')


# if len(sys.argv) < 4:
#     print('python group-needlep.py <train_folder> <groupsize> <mytar_save_folder>')
#     print('example: python group-needle.py ~/data/test-accuracy/imagenette2/train 4 ~/data/test-accuracy/mytar/train')
#     exit()

train_folder = sys.argv[1]
compress_level = int(sys.argv[2])
compress_save_folder = sys.argv[3] + '/{}/'.format(compress_level)

os.makedirs(compress_save_folder, exist_ok=True)

classes, class_to_idx = find_classes(train_folder)
print("classes: \n {} \n class_to_idx: \n {}".format(classes, class_to_idx))

for class_name in classes:
    os.makedirs(os.path.join(compress_save_folder, class_name), exist_ok=True)


instances = make_dataset(train_folder, class_to_idx, IMG_EXTENSIONS, None)
# print(instances)
print(len(instances))

for instance in instances:
    original_path = os.path.join(train_folder, instance)
    with open(original_path, 'rb') as reader:
        data = reader.read()
        iodata = io.BytesIO(data)
        img = Image.open(iodata)
        print('data size: {}'.format(len(data)))
        # print('compressed_data size: {}'.format(len(compressed_data)))
        img.save(compress_save_folder + instance + '.png', optimize=True, quality=100)
        # img.save(compress_save_folder + instance + '.JPEG', quality=100)
