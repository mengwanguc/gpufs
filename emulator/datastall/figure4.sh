#!/bin/bash
set -e

gpu_type="p100"
model="resnet18"
limits=("2g" "4g" "6g" "8g" "10g" "12g")
batch_size="256"
n_workers="1"
data_path="~/data/imagenette2"
gpu_count="4"

# set up control group
group_name="myGroup"
sudo cgcreate -g memory:$group_name
sudo chown -R ${USER} /sys/fs/cgroup/memory/$group_name

for limit in ${limits[@]}; do
    echo "Profiling model $model with $limit memory limit"

    # place the limit
    sudo bash -c "echo $limit > /sys/fs/cgroup/memory/$group_name/memory.limit_in_bytes"

    # flush memory & caches
    echo "Flushing memory/cache"
    sudo ./clear-cache.sh

    # run training with limited memory (https://unix.stackexchange.com/questions/44985/limit-memory-usage-for-a-single-linux-process)
    echo "running training"

    cgexec -g memory:$group_name python main-measure-time-emulator.py --gpu-type=$gpu_type --gpu-count=$gpu_count --arch=$model --epochs 2 --emulator-version=1 -j $n_workers $data_path &> outputsfig4/output$limit.txt
    
    # check how much memory the dataset was actually using
    # NOTE this isn't entirely accurate since the amount can vary throughout, and the amount at the end may not be representative/precise/etc. 
    echo "checking memory usage..."
    vmtouch $data_path/train &> outputsfig4/cache_result$limit.txt
    echo
done

# tear down the control group
sudo cgdelete memory:$group_name