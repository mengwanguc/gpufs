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

