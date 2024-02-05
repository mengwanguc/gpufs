import os
import shutil
import sys

originals = ['n01440764',
            'n02102040',
            'n02979186',
            'n03000684',
            'n03028079',
            'n03394916',
            'n03417042',
            'n03425413',
            'n03445777',
            'n03888257']

def duplicate_folders_in_directory(dir, start_index, end_index):
    for item in originals:
        item_path = os.path.join(dir, item)
        if os.path.isdir(item_path):
            for i in range(start_index, end_index+1):  # 10 iterations for 10 copies
                duplicate_folder_name = f"{item}_copy_{i}"
                duplicate_folder_path = os.path.join(dir, duplicate_folder_name)
                if not os.path.exists(duplicate_folder_path):
                    shutil.copytree(item_path, duplicate_folder_path)
                    print(f"Created copy {i} for folder: {item}")
                else:
                    print(f"Copy {i} already exists for folder: {item}")

if __name__ == "__main__":
    if len(sys.argv) < 3+1:
        print('python duplicate.py [dir] [start_index] [end_index]')
        exit(0)
    dir = sys.argv[1]
    start_index = int(sys.argv[2])
    end_index = int(sys.argv[3])
    duplicate_folders_in_directory(dir, start_index, end_index)