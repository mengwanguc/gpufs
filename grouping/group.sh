#!/bin/bash
for i in 32 1024
do
  echo "doing grouping mytar and tar for group size $i"
  python group-needle.py /home/cc/data/imagenette2/train/ $i ~/data/imagenette2/mytar/train
done