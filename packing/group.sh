#!/bin/bash
for i in 32 1024
do
  echo "doing grouping mytar and tar for group size $i"
  python group-needle.py /home/cc/data/imagenet/train/ $i ~/data/imagenet/mytar/train
done