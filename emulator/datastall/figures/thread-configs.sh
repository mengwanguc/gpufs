#!/bin/bash
set -e

gpu_type="p100"
model="resnet18"
batch_size="256"
limit="unlimited"
n_workers="4"
n_threads=(1 2 4 6 8 10 12 14 16)
data_path="/home/cc/data/test-utilization/imagenette2"

# set up control group
group_name="gpufs"

# move to the the emulator/datastall/ folder
cd ..

for threads in ${n_threads[@]}; do
    echo "Profiling model $model with $limit GB memory limit and $n_workers workers ($threads threads ea.)"

    # set up control group
    sudo cgcreate -g memory:$group_name
    sudo chown -R ${USER} /sys/fs/cgroup/memory/$group_name

    # place the memory limit
    sudo bash -c "echo $limit > /sys/fs/cgroup/memory/$group_name/memory.limit_in_bytes"

    # flush memory & caches
    echo "Flushing memory/cache"
    sudo ~/gpufs/exp/clear-cache.sh

    # run training with limited memory (https://unix.stackexchange.com/questions/44985/limit-memory-usage-for-a-single-linux-process)
    echo "running training"
    cgexec -g memory:$group_name python main-measure-time-emulator.py --load-threads $threads --emulator-version=1 -j 4 --epoch 2 --workers $n_workers --gpu-count 8 --gpu-type $gpu_type -a $model --batch-size $batch_size --profile-batches -1 $data_path
	
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
    mv ./$gpu_type/$model-batch$batch_size.csv ./$gpu_type/$model-$batch_size-batch_size-$n_workers-workers-$threads-threads-$limit-limit-$usage-usage-$cached-cached.csv
    echo

    # tear down the control group
    sudo cgdelete memory:$group_name
    
done
