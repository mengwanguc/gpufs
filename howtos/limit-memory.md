Google is always your best friend. I learned it by googling and following the steps 
in https://unix.stackexchange.com/questions/44985/limit-memory-usage-for-a-single-linux-process.

Here are detailed steps that I used to limit the memory of the training application.

1. Install cgroup

```
sudo apt install -y cgroup-tools
```


2. Create a group for which you will limit memory

```
sudo cgcreate -g memory:myGroup

# Change the permission of myGroup folder. Make it accessible by user "cc"
sudo chown -R cc /sys/fs/cgroup/memory/myGroup

# set limit to 5g
echo 5g > /sys/fs/cgroup/memory/myGroup/memory.limit_in_bytes
```

3. Run the application under the control group:

```
cgexec -g memory:myGroup python main-original.py /home/cc/data/test-accuracy/imagenette2
```

4. use "vmtouch" to monitor the cache percentage of the data.
