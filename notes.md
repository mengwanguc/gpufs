# oct 10 monday

for alexnet, when we use progress display every batch:
step 36  total time: 32.165523529052734  data time: 2.5077948570251465  display time: 7.392908573150635  move_time: 0.005036830902099609 compute_time: 6.739538669586182 optimize_time: 15.368357419967651, acc_time: 0.15094399452209473

when we don't display:
step 36  total time: 31.152629137039185  data time: 2.1425728797912598  display time: 0.0014476776123046875  move_time: 0.007977008819580078 output_time: 13.441510200500488 loss_time: 0.008159637451171875 optimize_time: 15.374119520187378, acc_time: 0.17546343803405762

We can see, if we display, display takes 7 sec, which is too much. If we don't display, then the total training time is the same, and that 7 sec is spent in computing output.

So what's that 7 sec for? Can we optimize it?
