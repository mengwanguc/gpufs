import os
import shutil

def duplicate_folders_in_current_directory():
    current_directory = os.getcwd()
    all = os.listdir(current_directory)
    for item in all:
        item_path = os.path.join(current_directory, item)
        if os.path.isdir(item_path):
            for i in range(1, 9):  # 10 iterations for 10 copies
                duplicate_folder_name = f"{item}_copy_{i}"
                duplicate_folder_path = os.path.join(current_directory, duplicate_folder_name)
                if not os.path.exists(duplicate_folder_path):
                    shutil.copytree(item_path, duplicate_folder_path)
                    print(f"Created copy {i} for folder: {item}")
                else:
                    print(f"Copy {i} already exists for folder: {item}")

if __name__ == "__main__":
    duplicate_folders_in_current_directory()