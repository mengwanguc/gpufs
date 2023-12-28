#!/bin/bash
set +e

node_count=$1
node_id=$2
node_master_ip=$3

gpu_type="p100"
gpu_count="4"
model="alexnet"
memory_limit=$((11 * 1024 * 1024 * 1024)) # should be ~65%-ish cached of imagenette
batch_size="256"
n_workers="24"
data_path="/home/cc/data/imagenette2"

# set up control group
group_name="gpufs"

# move the the emulator/datastall/ folder
cd ../..

###############################

echo "Profiling model $model with $gpu_count $gpu_type GPUs. $node_count nodes, id=$node_id."
sudo bash -c "sync; echo 3 > /proc/sys/vm/drop_caches"

# set up control group
sudo cgcreate -g memory:$group_name
sudo chown -R ${USER} /sys/fs/cgroup/memory/$group_name
sudo bash -c "echo $memory_limit > /sys/fs/cgroup/memory/$group_name/memory.limit_in_bytes"

# run training with limited memory (https://unix.stackexchange.com/questions/44985/limit-memory-usage-for-a-single-linux-process)
echo "running training"
export GLOO_SOCKET_IFNAME=eno1
cgexec -g memory:$group_name python main-measure-time-emulator.py --gpu-type=$gpu_type --gpu-count=$gpu_count --epoch 2 --skip-epochs=1 --workers $n_workers --arch=$model --batch-size $batch_size --profile-batches -1 --dist-url tcp://$node_master_ip:12345 --dist-backend gloo --world-size $node_count --rank $node_id $data_path

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
mv ./$gpu_type/$model-batch$batch_size.csv ./$gpu_type/$model-$batch_size-batch_size-$n_workers-workers-$gpu_count-gpus-$limit-limit-$usage-usage-$cached-cached-$node_count-nodes-$node_id-id.csv
echo

# tear down the control group
sudo cgdelete memory:$group_name
