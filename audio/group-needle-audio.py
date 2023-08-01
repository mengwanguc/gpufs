import sys
import os
import torch
from typing import Any, Callable, cast, Dict, List, Optional, Tuple
from os.path import basename
import tarfile


def has_file_allowed_extension(filename: str, extensions: Tuple[str, ...]) -> bool:
    """Checks if a file is an allowed extension.
    Args:
        filename (string): path to a file
        extensions (tuple of strings): extensions to consider (lowercase)
    Returns:
        bool: True if the filename ends with one of given extensions
    """
    print("extensions ->", extensions)
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
    print("directory ->", directory)
    both_none = extensions is None and is_valid_file is None
    print("both_none ->", directory)
    both_something = extensions is not None and is_valid_file is not None
    print("both_something ->", directory)
    if both_none or both_something:
        raise ValueError("Both extensions and is_valid_file cannot be None or not None at the same time")
    if extensions is not None:
        def is_valid_file(x: str) -> bool:
            return has_file_allowed_extension(x, cast(Tuple[str, ...], extensions))
    is_valid_file = cast(Callable[[str], bool], is_valid_file)
    print("is_valid_file ->", is_valid_file)
    for target_class in sorted(class_to_idx.keys()):
        print("target_class ->", target_class)
        class_index = class_to_idx[target_class]
        target_dir = os.path.join(directory, target_class)
        print("target_dir ->", target_dir)
        if not os.path.isdir(target_dir):
            continue
        for root, _, fnames in sorted(os.walk(target_dir, followlinks=True)):
            print("fnames -> ",fnames)
            for fname in sorted(fnames):
                path = os.path.join(root, fname)
                print("path -> ", path)
                print("is_valid_file(path) ->", is_valid_file(path))
                if is_valid_file(path):
                    item = path, target_class
                    print("item ->", item)
                    instances.append(item)
    return instances





audio_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.ppm', '.bmp', '.pgm', '.tif', '.wav',
                  '.tiff', '.webp', '.pickle', '.zip', 'tar', 'mytar')


if len(sys.argv) < 4:
    print('python group-needle-audio.py <train_folder> <groupsize> <mytar_save_folder>')
    print('example: python group-needle-audio.py ~/gpufs/audio/SpeechCommands-small/speech_commands_v0.02 4 ~/gpufs/audio/grouped-data-audio')
    exit()

train_folder = sys.argv[1]
print("train_folder ->", train_folder)
group_size = int(sys.argv[2])
print("group_size ->", group_size)
mytar_save_folder = sys.argv[3] + '/{}/'.format(group_size)
print("mytar_save_folder ->", mytar_save_folder)

os.makedirs(mytar_save_folder, exist_ok=True)

classes, class_to_idx = find_classes(train_folder)
print("classes: \n {} \n class_to_idx: \n {}".format(classes, class_to_idx))

instances = make_dataset(train_folder, class_to_idx, audio_EXTENSIONS, None)
print(instances)
print("instances -> ", instances[0])
print("number of images: {}".format(len(instances)))

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
        audiodata = b''
        offset = 0
        metadata += '{},{}\n'.format(mytar_name,group_size)
        for j in range(group_size):
            idx = permutation[i*group_size + j]
            audio_path, target_class = instances[idx]
            audio_size = os.path.getsize(audio_path)
            metadata += '{},{},{},{},{}\n'.format(j, target_class, offset, audio_size,audio_path)
            offset += audio_size
            with open(audio_path, 'rb') as reader:
                audio = reader.read()
                audiodata += audio
        with open(mytar_save_folder + mytar_name, 'wb') as writer:
            writer.write(audiodata)


    metadata_writer.write(metadata)


print("group_size: {} group num: {}".format(
           group_size, group_num))