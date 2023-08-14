#!/bin/bash
set -e

gpu_type="p100"
model="alexnet"
n_workers=4
batch_size=256
data_path="/home/cc/data/test-accuracy/imagenette2"
# limit="9G"
superbatch_configs=(1 2 4 8 16)
prefetch_factor=2

# set up control group
group_name="gpufs"

# move to the the emulator/datastall/ folder
cd ../..

for superbatch in ${superbatch_configs[@]}; do
    echo "Profiling model $model with $n_workers workers"

    # set up control group
    sudo cgcreate -g memory:$group_name
    sudo chown -R ${USER} /sys/fs/cgroup/memory/$group_name

    # place the limit
    # sudo bash -c "/usr/bin/echo $limit > /sys/fs/cgroup/memory/$group_name/memory.limit_in_bytes"

    # flush memory & caches
    echo "Flushing memory/cache"
    sync
    sudo bash -c "/usr/bin/echo 3 > /proc/sys/vm/drop_caches"

    # run training with limited memory (https://unix.stackexchange.com/questions/44985/limit-memory-usage-for-a-single-linux-process)
    echo "running training"
    cgexec -g memory:$group_name python main-measure-time-emulator.py --use-async True --super-batch-size $superbatch --prefetch-factor $prefetch_factor --skip-epochs 0 --emulator-version=1 -j 4 --epoch 1 --workers $n_workers --gpu-count 1 --gpu-type $gpu_type -a $model --batch-size $batch_size --profile-batches -1 $data_path
	
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
    mv ./$gpu_type/$model-batch$batch_size.csv ./$gpu_type/script-$model-$batch_size-batch_size-$superbatch-superbatch-$n_workers-workers-$limit-limit-$usage-usage-$cached-cached-async.csv
    mv ./pytorch_timing.csv ./$gpu_type/pytorch-$model-$batch_size-batch_size-$superbatch-superbatch-$n_workers-workers-$limit-limit-$usage-usage-$cached-cached-async.csv
    echo

    # tear down the control group
    sudo cgdelete memory:$group_name
    
done
