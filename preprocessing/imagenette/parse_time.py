import sys
import json
from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np

fig = plt.figure()
lines = []

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 12

with open(sys.argv[1], 'r') as f:
    lines = f.readlines()


keys = {'filesize': 'filesize', 
        'after decoding': 'after decoding', 
        'original shape': 'original shape', 
        'after RandomResizedCrop': 'after RandomResizedCrop(size=(224, 224), scale=(0.08, 1.0), ratio=(0.75, 1.3333), interpolation=bilinear)', 
        'after RandomHorizontalFlip': 'after RandomHorizontalFlip(p=0.5)', 
        'after ToTensor': 'after ToTensor()', 
        'after Normalize': 'after Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])',
        'time RandomResizedCrop': 'time for RandomResizedCrop(size=(224, 224), scale=(0.08, 1.0), ratio=(0.75, 1.3333), interpolation=bilinear)', 
        'time RandomHorizontalFlip': 'time for RandomHorizontalFlip(p=0.5)', 
        'time ToTensor': 'time for ToTensor()', 
        'time Normalize': 'time for Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])',}


all_size_dict = []

filesizes = []
after_decoding_sizes = []
after_random_resized_crop_sizes = []
after_random_horizon_flip_sizes = []
after_totensor_sizes = []
after_normalize_sizes = []
time_random_resized_crop_sizes = []
time_random_horizon_flip_sizes = []
time_totensor_sizes = []
time_normalize_sizes = []
img_load_times = []
img_convert_times = []

for line in lines:
    if '\'filesize\'' in line and not 'after Resize' in line:
        size_dict = eval(line.strip())
        all_size_dict.append(size_dict)
        filesizes.append(int(size_dict[keys['filesize']]))
        after_decoding_sizes.append(int(size_dict[keys['after decoding']]))
        after_random_resized_crop_sizes.append(int(size_dict[keys['after RandomResizedCrop']]))
        after_random_horizon_flip_sizes.append(int(size_dict[keys['after RandomHorizontalFlip']]))
        after_totensor_sizes.append(int(size_dict[keys['after ToTensor']]))
        after_normalize_sizes.append(int(size_dict[keys['after Normalize']]))
        time_random_resized_crop_sizes.append(float(size_dict[keys['time RandomResizedCrop']])*1000)
        time_random_horizon_flip_sizes.append(float(size_dict[keys['time RandomHorizontalFlip']])*1000)
        time_totensor_sizes.append(float(size_dict[keys['time ToTensor']])*1000)
        time_normalize_sizes.append(float(size_dict[keys['time Normalize']])*1000)
    elif 'image_open_time' in line:
        substrs = line.strip().split('\t')
        img_load_time = float(substrs[2].split(':')[1]) * 1000
        img_convert_time = float(substrs[3].split(':')[1]) * 1000
        img_load_times.append(img_load_time)
        img_convert_times.append(img_convert_time)

num_training_images = len(filesizes)
training_img_load_times = img_load_times[0:num_training_images]
training_img_convert_times = img_convert_times[0:num_training_images]
training_decoding_times = [training_img_load_times[i] + training_img_convert_times[i] for i in range(len(training_img_load_times))]


def cdf(x, *args, **kwargs):
    x, y = sorted(x), np.arange(len(x)) / len(x)
    return plt.plot(x, y, *args, **kwargs)

# sns.ecdfplot(data = filesizes, cumulative = True, label = "JPG file size")
cdf(training_decoding_times, label = "Time decoding", color='red')
cdf(time_random_resized_crop_sizes, label = "Time RandomResizedCrop", color='orange')
cdf(time_random_horizon_flip_sizes, label = "Time RandomHorizontalFlip", color='green')
cdf(time_totensor_sizes, label = "Time ToTensor", color='blue')
cdf(time_normalize_sizes, label = "Time Normalize", color='purple')


plt.xlim(0, 10)
plt.ylim(0, 1.0)

xticks = range(0,10)
plt.xticks(xticks)
plt.xlabel("Time (ms)")
plt.ylabel("CDF")
plt.title("CDF of time spent in each preprocessing step")

plt.legend()


fig.set_size_inches(8, 4)
fig.set_dpi(300)

plt.savefig('times.png', bbox_inches='tight')





