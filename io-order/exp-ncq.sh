#!/bin/bash

# for i in 1 2 4 8 16 32 64
# # for i in 1
# do
#   echo "unsort 10000 IO. Threads: $i"
#   sudo bash clear-bash.sh
#   ./read filepaths/imagenet_train_file_paths $i 0 1 10000
#   sudo bash clear-bash.sh
# done


for i in 1 2 4 8 16 32 64
# for i in 1
do
  echo "all sort lba 10000 IO. Threads: $i"
  sudo bash clear-bash.sh
  ./read filepaths/imagenet_train_file_paths $i 4 1 10000
  sudo bash clear-bash.sh
done