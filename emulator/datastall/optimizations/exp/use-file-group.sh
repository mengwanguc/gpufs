#!/bin/bash
sudo bash clear-cache.sh
python main-measure-time-emulator.py  --epoch 1 --profile-batches -1 --workers 8 --gpu-type=p100 --gpu-count=2 --arch=alexnet --emulator-version=1 --img_per_tar=1 ~/data/test-grouping/imagenette2

for i in 1 2 4 8 16 32 64
do
  echo "training using  for group size $i"
  sudo bash clear-cache.sh
  python main-measure-time-emulator.py  --epoch 1 --profile-batches -1 --workers 8 --gpu-type=p100 --gpu-count=2 --arch=alexnet --emulator-version=1 --img_per_tar=$i --use-file-group=True ~/data/test-grouping/imagenette2
done