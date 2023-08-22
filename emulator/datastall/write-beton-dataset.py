import argparse
import os

from ffcv.writer import DatasetWriter
from ffcv.fields import RGBImageField, BytesField

import torch
import torch.nn as nn
import torch.nn.parallel
import torch.backends.cudnn as cudnn
import torch.distributed as dist
import torch.optim
from torch.optim.lr_scheduler import *
import torch.multiprocessing as mp
import torch.utils.data
import torch.utils.data.distributed
import torchvision.transforms as transforms
import torchvision.datasets as datasets
import torchvision.models as models

parser = argparse.ArgumentParser(description='PyTorch -> FFCV Dataset Converter')
parser.add_argument('dir_in', metavar='DIR_IN', help='path to dataset')
parser.add_argument('dir_out', metavar='DIR_OUT', help='path to write FFCV dataset at')

def main():
    args = parser.parse_args()

    dataset = datasets.ImageFolder(
        args.dir_in,
        # transforms.Compose([
        #     transforms.RandomResizedCrop(224),
        #     transforms.RandomHorizontalFlip(),
        #     transforms.ToTensor(),
        #     normalize,
        # ]),
        use_file_group = args.use_file_group,
        group_size = args.img_per_tar
    )

    writer = DatasetWriter(
        args.dir_out,
        {
            'image': RGBImageField(),
            'label': BytesField(),
        }
    )

    writer.from_indexed_dataset(dataset)