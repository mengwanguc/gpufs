#!/bin/bash

for i in 1000000 100000 10000 1000 100
# for i in 10000 1000 100
# for i in 1
do
  echo "all sort lba 1000000 IO. Threads: $i"
  sudo bash clear-bash.sh
  ./read filepaths/imagenet_train_file_paths 32 4 0 $i
  sudo bash clear-bash.sh
done


for i in 10000
# for i in 1
do
  echo "all sort lba 1000000 IO. Threads: $i"
  sudo bash clear-bash.sh
  ./read filepaths/imagenet_train_file_paths 32 0 0 $i
  sudo bash clear-bash.sh
done