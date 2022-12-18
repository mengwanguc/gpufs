# Dec 17

## pin inodes to cache

`locate ~/data/imagenet/train/`

## control memory usage

https://unix.stackexchange.com/questions/44985/limit-memory-usage-for-a-single-linux-process

## control inode cache

https://serverfault.com/questions/338097/tuning-linux-cache-settings-for-inode-caching


# drop caches

https://unix.stackexchange.com/questions/17936/setting-proc-sys-vm-drop-caches-to-clear-cache

basically, if we want to drop all, we do: `sync; echo 3 > /proc/sys/vm/drop_caches`

if we want to keep directories and inodes cache, we do: `sync; echo 1 > /proc/sys/vm/drop_caches`

# Nov 28

### data size

tf.data: A Machine Learning Data Processing Framework
- 70% jobs' data size decreases after preprocessing. Why don't we store them directly?
- cache preprocessed data?
- some datasets use "shuffle" transformation, so should be excluded.
- I remember gandiva searches all ml jobs on github?
- Figure 10 showed that data preprocessing reduces the volume of data for 75% of jobs. For 14% of jobs, the volume of data fed into the model for training is less than 10% of bytes read from storage. As input data for ML jobs commonly resides in remote storage, such as a distributed file system or cloud object store, this means that more data than necessary is sent over the network during ML training. Designing ML data processing systems that apply projections closer to storage is a promising way
- **they already pipeline data preprocessing and IO in tensorflow!**

Evaluating Block-level Optimization through the IO Path
- The queue depth at the disk drive level is a parame- ter set at the device driver and often set to 4 (the default value for many SCSI device drivers). The queue depth at the disk is commonly kept low to avoid request starva- tion, because disk drive scheduling introduces variability in request response time, which can be controlled easily by the operating system at the device driver with algo- rithms such as Deadline but not at the disk drive level.

where is disk schedulign implemented:
https://stackoverflow.com/questions/49220089/where-is-disk-scheduling-implemented

# Nov 27

### tagged command queueing:
- http://www.stbsuite.com/support/virtual-training-center/introduction-to-command-queuing


where is disk scheduling implemented: https://stackoverflow.com/questions/49220089/where-is-disk-scheduling-implemented
>In the mid-1980's it started to become common for disk drives to provide a logical I/O interface. The device driver no longer saw disks/platters/sectors. Instead, it just saw an array of logical blocks. The drive took care of physical locations and redirecting of bad blocks (tasks that the operating system used to handle). This allowed single device driver to manage multiple types of devices, sharing the same interface and differing only in the number of logical blocks.

# Nov 26

estimate disk drive latency: https://www.fsl.cs.sunysb.edu/docs/ospert-iosched/map-ioscheduler.pdf

Question for https://www.usenix.org/system/files/hotcloud19-paper-kakaraparthy.pdf

- To generate one reservior, do you need to read through the entire dataset?
- How often do you re-fill the reservior? Do you re-fill it per batch, or per reservior (i.e. 400 batches in the example experiment setup.)
- Is the source code open?

### my thoughts

- We can also have a reservior of e.g. 400 groups in memory. We can further randomize the reservior.
- In pytorch, for every epoch, the loading of the first batch is usually slow, because multiple processing and it's not overlapped by gpu time. So maybe we should have a data loader which can fill the reservior for the next epoch.
- use a dedicated cpu to read data
- Since deep learning training has deterministic training time and order, the remote cloud storage server can prepare the data in advance based on better scheduling.

### From Graphene:{Fine-Grained}{IO} Management for Graph Computing
- For instance, Linux exploits a linked list called pluglist to batch and submit the IO requests [8], in particular, the most recent Linux kernel 4.4.0 supports 16 requests in a batch
- IO merging...
- IO sorting
- Graphene pins IO and computing threads to the CPU socket that is close to the SSD they are working on. This NUMA-aware arrangement reduces the communication overhead between IO thread and SSD, as well as IO and computing threads. Our test shows that this can improve the performance by 5% for various graphs

### documentation
linux io scheduler
https://www.kernel.org/doc/html/v6.0/block/index.html

[PATCH 11/16] blk-mq: improve plug list sorting: https://lkml.iu.edu/hypermail/linux/kernel/1810.3/04456.html

# Nov 25

### my thoughts

- Can we sort the IO requests to reduce seek time?
- In IO scheduling, the io scheduler needs to switch between different processes, which might not be a good ordering. Can we disable the switch? Or maybe we can set the time slice to very large.

https://wiki.ubuntu.com/Kernel/Reference/IOSchedulers

https://www.oreilly.com/library/view/linux-device-drivers/0596000081/ch12s04.html



# Nov 3

random read on ssd:
https://superuser.com/questions/1108034/why-are-4k-reads-in-hdd-ssd-benchmarks-slower-than-writes

https://superuser.com/questions/1325962/sequential-vs-random-i-o-on-ssds

os takes time to prepare io request, which may be cpu intensive???

---

gzip doesn't help to compress image, because JEPG images are already compressed.

openimages use jpg

tradeoff between io and cpu

free music use mp3 (compressed)

---

faster than pillow: https://github.com/jbaiter/jpegtran-cffi

---

We can allow users to specify an acceptable quality ratio

so we allow a tradeoff between training speed and accuracy


by using profiling, we can show user the training time given ratio.

--

Other sequentail methods:

TFRecord???

dali-seq???



# Nov 2

Set cpu constraints for a namespace:
https://kubernetes.io/docs/tasks/administer-cluster/manage-resources/cpu-constraint-namespace/

adaptdl:

https://adaptdl.readthedocs.io/en/latest/commandline/tensorboard.html

Vijay's paper on gpu scheduling:

https://www.usenix.org/system/files/osdi22-mohan.pdf

# Nov 1

Tensorflow already implements async cpu-to-gpu transfer:
https://github.com/tensorflow/tensorflow/issues/5722

This person answered something that prefetch cpu-to-gpu, but does pytorch really supports that?
https://stackoverflow.com/questions/63460538/proper-usage-of-pytorchs-non-blocking-true-for-data-prefetching

okay it's done in pytorch lightning... :(
https://github.com/Lightning-AI/lightning/issues/1404

Why do we do preprocessing during every batch? Why don't we just do it once?

In-storage computation???

data compression?

When IO is bottleneck, we can use compressed data, to save memory and speed up data read. 

The tradeoff is that we need to do extra data uncompressing, which adds cpu overhead.

We can even move overhead to gpu (e.g. using dali https://developer.nvidia.com/blog/rapid-data-pre-processing-with-nvidia-dali/)

Deep learning scheduler:

https://github.com/mozilla/snakepit



# Oct 11 Tuesday
alexnet self forward time: 6.85730504989624

Epoch: [0][37/37]       Loss 0.0000e+00 (0.0000e+00)    Acc@1  12.50 (  9.57)   Acc@5  46.67 ( 48.57)

step 36  total time: 32.020240783691406  data time: 2.264488935470581  display time: 7.43507981300354  move_time: 0.006020069122314453 output_time: 6.861251592636108 loss_time: 0.011179924011230469 optimize_time: 15.280409336090088, acc_time: 0.16044950485229492


alexnet self forward time: 13.473725080490112

step 36  total time: 31.30919909477234  data time: 2.2561912536621094  display time: 0.001252889633178711  move_time: 0.005376338958740234 output_time: 13.477182388305664 loss_time: 0.012679576873779297 optimize_time: 15.37448239326477, acc_time: 0.18066024780273438


images = images.cuda(args.gpu, non_blocking=True)

Here "non-blocking" means that the data transfer from cpu to gpu is done asynchronously to the host
https://github.com/mengwanguc/pytorch-meng/blob/199358ef854f8ad4612d89bff429fe6fd9105d5d/torch/_utils.py

However, I don't think it's asynchronous to the gpu computation nor data loader.
https://discuss.pytorch.org/t/should-we-set-non-blocking-to-true/38234

However, I think it's possible according to nvidia:

https://developer.nvidia.com/blog/how-overlap-data-transfers-cuda-cc/

https://stackoverflow.com/questions/65932328/pytorch-while-loading-batched-data-using-dataloader-how-to-transfer-the-data-t

https://spell.ml/blog/pytorch-training-tricks-YAnJqBEAACkARhgD

https://pytorch.org/docs/stable/notes/cuda.html#cuda-memory-pinning

https://www.telesens.co/2019/02/16/efficient-data-transfer-from-paged-memory-to-gpu-using-multi-threading/

Seems they have already tried to pipeline data transfer and training.
However, some layers, e.g. conv2d, will require the whole batch to be ready in order to do the computation.
In this case, the pipelining doesn't work.

However, while we are doing computation for 1st batch, we can try to transfer the data of 2nd batch to gpu.

## TODO

Need to check it on cuda 11


----
how to compare two commits:

https://github.com/mengwanguc/torchvision-meng/compare/859a535f53be41554d8da45c4b6172089096eb7f..21a5611c9eb7bdd41b915d335fa5e044451db5df

https://github.com/mengwanguc/pytorch-meng/compare/2564cc7a1d5a8bd4ae1d1a045654c576e568e470..199358ef854f8ad4612d89bff429fe6fd9105d5d

## TODO:

Today fixed class_index issue for my_tar. Need to apply the same fix to other scenarios e.g. is_async etc.


# Oct 10 Monday

for alexnet, when we use progress display every batch:

step 36  total time: 32.165523529052734  data time: 2.5077948570251465  display time: 7.392908573150635  move_time: 0.005036830902099609 compute_time: 6.739538669586182 optimize_time: 15.368357419967651, acc_time: 0.15094399452209473

when we don't display:

step 36  total time: 31.152629137039185  data time: 2.1425728797912598  display time: 0.0014476776123046875  move_time: 0.007977008819580078 output_time: 13.441510200500488 loss_time: 0.008159637451171875 optimize_time: 15.374119520187378, acc_time: 0.17546343803405762

We can see, if we display, display takes 7 sec, which is too much. If we don't display, then the total training time is the same, and that 7 sec is spent in computing output.

So what's that 7 sec for? Can we optimize it?

``output = model(images)``

Here ``model`` is the model class. For example, it can be `Alexnet`.

`model(images)` will call `__call__` function inside torch/nn/modules/module.py: https://github.com/mengwanguc/pytorch-meng/blob/main/torch/nn/modules/module.py#L866

