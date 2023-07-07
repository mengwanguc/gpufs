#!/bin/bash
set -e

gpu_type="p100"
# "shufflenet_v2_x0_5" "resnet18" "vgg11"
models=("shufflenet_v2_x0_5" "resnet18" "squeezenet1_1" "vgg11")
# Saved cache size: "2g" "4g" "6g" "8g" "10g" "12g" "14g"
# to reach 35% of figrue 3, I calculated that it should be about 3.2GB = 3200MB
limit="14g"
batch_size="256"
n_workers="24"
data_path="~/data/imagenette2"
gpu_count="8"

# set up control group
group_name="myGroup"
sudo cgcreate -g memory:$group_name
sudo chown -R ${USER} /sys/fs/cgroup/memory/$group_name

echo "Profiling model $model with $limit memory limit"
# place the limit which will always be 6G in this case
sudo bash -c "echo $limit > /sys/fs/cgroup/memory/$group_name/memory.limit_in_bytes"

cgexec -g memory:$group_name python main-measure-time-emulator.py  --epoch 1 --profile-batches -1 --workers 4 --gpu-type=$gpu_type --gpu-count=$gpu_count --arch=resnet18 --emulator-version=1 ~/data/imagenette2 &> outputsfig3/output_fill_cache.txt

for model in ${models[@]}; do
    # flush memory & caches
    #echo "Flushing memory/cache"
    #sudo ./clear-cache.sh

    # run training with limited memory (https://unix.stackexchange.com/questions/44985/limit-memory-usage-for-a-single-linux-process)
    echo "running training"
    
    #cgexec -g memory:$group_name python main-measure-time-emulator.py --gpu-type=$gpu_type --gpu-count=$gpu_count --arch=$model --epochs 2 --emulator-version=1 -j $n_workers $data_path &> outputsfig4/output$limit.txt
    cgexec -g memory:$group_name python main-measure-time-emulator.py  --epoch 1 --profile-batches -1 --workers $n_workers --gpu-type=$gpu_type --gpu-count=$gpu_count --arch=$model --emulator-version=1 ~/data/imagenette2 &> outputsfig3/output_100$model.txt
    # check how much memory the dataset was actually using
    # NOTE this isn't entirely accurate since the amount can vary throughout, and the amount at the end may not be representative/precise/etc. 
    echo "checking memory usage..."
    vmtouch ~/data/imagenette2/train/ &> outputsfig3/cache_result_100$model.txt
    echo
done

# tear down the control group
sudo cgdelete memory:$group_name