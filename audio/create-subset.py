import os

# Path to the root directory of your dataset
dataset_root = "/home/cc/gpufs/audio/SpeechCommands/speech_commands_v0.02"

# Manually specify the number of samples for training and testing
num_train_samples = 10
num_test_samples = 5

# Initialize lists to store the file names for training and testing
train_files = []
test_files = []
classes_names = os.listdir(dataset_root)
print("os.listdir(dataset_root) ->", classes_names)
# classes_names.remove('validation_list.txt')
# classes_names.remove('testing_list.txt')
classes_names.remove('.DS_Store')
classes_names.remove('README.md')
classes_names.remove('LICENSE')
print("os.listdir(dataset_root) ->", classes_names)
# Loop through each class folder
for class_name in classes_names:
    class_path = os.path.join(dataset_root, class_name)
    
    # Get a list of all audio files in the class folder
    audio_files = [file for file in os.listdir(class_path) if file.endswith('.wav')]
    
    # Split the files into training and testing sets based on the specified number of samples
    train_files.extend([f"{class_name}/{file}" for file in audio_files[:num_train_samples]])
    test_files.extend([f"{class_name}/{file}" for file in audio_files[num_train_samples:num_train_samples + num_test_samples]])

# Save the file names into training.txt and testing.txt files
with open(dataset_root + '/testing_list.txt', 'w') as train_txt:
    for file in train_files:
        train_txt.write(file + '\n')

with open(dataset_root + '/validation_list.txt', 'w') as test_txt:
    for file in test_files:
        test_txt.write(file + '\n')