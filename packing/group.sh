#!/bin/bash
for i in 32
do
  echo "doing grouping mytar and tar for group size $i"
  python group-needle.py /home/cc/data/imagenet/ $i ~/data/imagenet/mytar/
done