#!/bin/bash
set -e

gpu_type="p100"
model="alexnet"
workers=(1 2 4 8)
batch_size="256"
data_path="/home/cc/data/test-utilization/imagenette2"

# set up control group
group_name="gpufs"

# move to the the emulator/datastall/ folder
cd ../..

for n_workers in ${workers[@]}; do
    echo "Profiling model $model with $n_workers workers"

    # set up control group
    sudo cgcreate -g memory:$group_name
    sudo chown -R ${USER} /sys/fs/cgroup/memory/$group_name

    # flush memory & caches
    echo "Flushing memory/cache"
    sudo ~/gpufs/exp/clear-cache.sh

    # run training with limited memory (https://unix.stackexchange.com/questions/44985/limit-memory-usage-for-a-single-linux-process)
    echo "running training"
    cgexec -g memory:$group_name python main-measure-time-emulator.py --skip-epochs 0 --emulator-version=1 -j 4 --epoch 1 --workers $n_workers --gpu-count 1 --gpu-type $gpu_type -a $model --batch-size $batch_size --profile-batches -1 $data_path
	
    # check how much memory the DATASET was actually using
    # NOTE this isn't entirely accurate since the amount can vary throughout, and the amount at the end may not be representative/precise/etc. 
    echo "checking % of dataset cached"
    cached=$(vmtouch $data_path | grep "Resident Pages" | awk 'NF>1{print $NF}')
    echo "... $cached cached\n"

    # check how much memory the entire cgroup was actually using
    echo "checking bytes of memory used"
    usage=$(cat /sys/fs/cgroup/memory/$group_name/memory.max_usage_in_bytes)
    echo "... $usage bytes\n"

    # save our output to a meaningful filename
    mv ./$gpu_type/$model-batch$batch_size.csv ./$gpu_type/$model-$batch_size-batch_size-$n_workers-workers-$limit-limit-$usage-usage-$cached-cached.csv
    echo

    # tear down the control group
    sudo cgdelete memory:$group_name
    
done
