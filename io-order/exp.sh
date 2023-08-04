#!/bin/bash

for i in 1 2 4 8 16 32 64
# for i in 1
do
  echo "unsort 10000 IO. Threads: $i"
  sudo bash clear-bash.sh
  ./read imagenet_train_file_paths $i 0 1
  sudo bash clear-bash.sh
done


for i in 1 2 4 8 16 32 64
# for i in 1
do
  echo "partial sort 10000 IO. Threads: $i"
  sudo bash clear-bash.sh
  ./read imagenet_train_file_paths $i 1 1
  sudo bash clear-bash.sh
done


for i in 1 2 4 8 16 32 64
# for i in 1
do
  echo "all sort 10000 IO. Threads: $i"
  sudo bash clear-bash.sh
  ./read imagenet_train_file_paths $i 2 1
  sudo bash clear-bash.sh
done

for i in 1 2 4 8 16 32 64
# for i in 1
do
  echo "all sort inode 10000 IO. Threads: $i"
  sudo bash clear-bash.sh
  ./read imagenet_train_file_paths $i 3 1
  sudo bash clear-bash.sh
done

for i in 1 2 4 8 16 32 64
# for i in 1
do
  echo "all sort lba 10000 IO. Threads: $i"
  sudo bash clear-bash.sh
  ./read imagenet_train_file_paths $i 4 1
  sudo bash clear-bash.sh
done