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
        'after Normalize': 'after Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])'}


all_size_dict = []

filesizes = []
after_decoding_sizes = []
after_random_resized_crop_sizes = []
after_random_horizon_flip_sizes = []
after_totensor_sizes = []
after_normalize_sizes = []

for line in lines:
    if 'filesize' in line and not 'after Resize' in line:
        size_dict = eval(line.strip())
        all_size_dict.append(size_dict)
        filesizes.append(int(size_dict[keys['filesize']]))
        after_decoding_sizes.append(int(size_dict[keys['after decoding']]))
        after_random_resized_crop_sizes.append(int(size_dict[keys['after RandomResizedCrop']]))
        after_random_horizon_flip_sizes.append(int(size_dict[keys['after RandomHorizontalFlip']]))
        after_totensor_sizes.append(int(size_dict[keys['after ToTensor']]))
        after_normalize_sizes.append(int(size_dict[keys['after Normalize']]))


def cdf(x, *args, **kwargs):
    x, y = sorted(x), np.arange(len(x)) / len(x)
    return plt.plot(x, y, *args, **kwargs)

# sns.ecdfplot(data = filesizes, cumulative = True, label = "JPG file size")
cdf(filesizes, label = "JPG File Size (Compressed)", color='blue')
cdf(after_decoding_sizes, label = "After Decoding (Decompress)", color='red')
cdf(after_random_resized_crop_sizes, label = "After RandomResizedCrop", color='green', linewidth=4)
cdf(after_random_horizon_flip_sizes, label = "After RandomHorizontalFlip", color='yellow', linestyle='--')
cdf(after_totensor_sizes, label = "After ToTensor", color='orange', linewidth=4)
cdf(after_normalize_sizes, label = "After Normalize", color='purple', linestyle='--')


plt.xlim(0, 1350000)
plt.ylim(0, 1.0)

xticks = range(0,1400000, 200000)
xticks_labels = [int(t/1000) for t in xticks]
plt.xticks(xticks, xticks_labels)
plt.xlabel("Image size (KB)")
plt.ylabel("CDF")
plt.title("CDF of image sizes after each preprocessing step")

plt.legend()


fig.set_size_inches(8, 4)
fig.set_dpi(300)

plt.savefig('sizes.png', bbox_inches='tight')





