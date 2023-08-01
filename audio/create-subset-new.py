import os
import shutil
import random

# Paths to the root directory of the original dataset and the lists
original_dataset_root = "/home/cc/gpufs/audio/SpeechCommands/speech_commands_v0.02"
validation_list_file = os.path.join(original_dataset_root, "validation_list.txt")
testing_list_file = os.path.join(original_dataset_root, "testing_list.txt")

# Paths to the root directory of the new dataset
new_dataset_root = "/home/cc/gpufs/audio"

# Create the new dataset directory
os.makedirs(new_dataset_root, exist_ok=True)

# Function to copy a specified number of random files from the original dataset to the new dataset
def copy_random_files_to_subset(file_list, source_dir, target_dir, num_samples):
    with open(file_list, 'r') as file:
        lines = file.readlines()
        random.shuffle(lines)
        for line in lines[:num_samples]:
            filename = line.strip()
            label = filename.split('/')[0]
            target_label_dir = os.path.join(target_dir, label)
            os.makedirs(target_label_dir, exist_ok=True)
            source_path = os.path.join(source_dir, filename)
            target_path = os.path.join(target_label_dir, filename.split('/')[-1])
            shutil.copy(source_path, target_path)

# Copy 10 random files to the new dataset for each subset (training, validation, and testing)
commands_dir = os.path.join(original_dataset_root)

# Copy random files to the training subset (include all files not listed in validation and testing)
for label in os.listdir(commands_dir):
    label_dir = os.path.join(commands_dir, label)
    filenames = os.listdir(label_dir)
    random.shuffle(filenames)
    for filename in filenames[:10]:
        source_path = os.path.join(label_dir, filename)
        target_path = os.path.join(new_dataset_root, "train", f"{label}/{filename}")
        shutil.copy(source_path, target_path)

# Copy 10 random files to the validation subset
copy_random_files_to_subset(validation_list_file, commands_dir, new_dataset_root, num_samples=10)

# Copy 10 random files to the testing subset
copy_random_files_to_subset(testing_list_file, commands_dir, new_dataset_root, num_samples=10)
