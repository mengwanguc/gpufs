#!/bin/bash
for i in 1 2 4 8 16 32 64
do
  echo "doing grouping mytar and tar for group size $i"
  python group-needle.py /home/cc/data/imagenette2/train/ $i
done