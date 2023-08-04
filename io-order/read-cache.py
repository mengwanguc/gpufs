import sys
import time
import os

from dataclasses import dataclass


total_files = 1281167
num_reads = 10000

open_time = 0
read_time = 0
batch_size = 10000





@dataclass
class Imagefile:
    path: str
    size: int

pathsfile = sys.argv[1]



imagefiles = []


with open(pathsfile, "r") as f:
    # file_size = os.path.getsize(pathsfile)
    lines = f.readlines()
    for line in lines:
        infos = line.strip().split(' ')
        imagefiles.append(Imagefile(infos[0], infos[1]))


with open(imagefiles[0].path, 'rb') as f:
    data = f.read()
    print(sys.getsizeof(data))

