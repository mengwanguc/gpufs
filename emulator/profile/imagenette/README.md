# README FIRST before doing experiments!!!

## NOTES

- When you install our custom "pytorch-meng" and "torchvision-meng", please use branches "original-pytorch" and "original-torchvision" respectively.

- Use "run-all.sh" to save your life when running experiments for a lot of models and batch sizes. See Step 1 to learn how to use it.



## Steps
<ol>
<!-- first step -->
<li> Run the experiments
<!-- if only run one experiment -->
<ul> 
<li>
To run a single experiment, use `main-measure-time.py`. Example:

`python main-measure-time.py --epoch 1 ~/data/test-accuracy/imagenette2 --gpu 0 --gpu-type p100 -a alexnet --batch-size 256`

This will produce a file `p100/alexnet-batch256.csv`.

Replace the parameters with your gpu-type (p100/v100/rtx6000/...), model type (alexnet/resnet101/...), batch size (256/128/64/...)

</li>

<!-- if run all experiments -->
<li>To run experiments for many models and batch sizes at once, use `run-all.sh`. Example

`bash run-all.sh`

Read `run-all.sh` to understand it. Modify it to replace gpu-type with your current gpu node type, and add/remove model types and batch sizes.

**NOTE**: I suggest you use `tmux` to run `run-all.sh` in the background. If you don't want what's `tmux` and how to use it, Google it. 
I also recommend you save the output into a file. For example, `bash run-all.sh &> output.log`. Don't commit this log file, but this file will be great for debugging purpose.

</li>

</ul>
</li>



<li>

Open the file in e.g. `p100/` folder, e.g. `p100/alexnet-batch256.csv`, copy the **numbers**, and paste into the google sheet:

https://docs.google.com/spreadsheets/d/1r2dfwMVD_5S8C_8em-hdN6r_iumH0bj4F2xWZKehUFc/edit#gid=0

The google sheet will compute the average and std of batches 1-10.

**Notes:**

- You might need to create new rows in the sheet for a new model. Just follow the style of existing records.

- It ignores batch 0 when computing average and std, because the values from batch 0 are very different from those
from other batches. But please still copy paste batch 0's numbers into the google sheet as a record.

- Sometimes the batch's memory requirement is too large to fit into GPU memory, and you'll see an error like `RuntimeError: CUDA out of memory. Tried to allocate 98.00 MiB (GPU 0; 15.90 GiB total capacity; 14.96 GiB already allocated; 33.75 MiB free; 15.16 GiB reserved in total by PyTorch)`.  When this happens, just put "N/A" in the google sheets. You'll need to reduce the batch size in order to reduce the memory requirement.

- If you are using `run-all.sh`, and see some `.csv` files are missing, that is probably caused by the `out of memory` error as mentioned above. So just go ahead check your output log file generated in step 1, e.g. `output.log`, and search for the model and batch size. If you see the `out of memory` error, then put `N/A`.

- If the computed relative std is larger than 5%, please mark it using bold and red color in the google sheet.

</li>

<li>
If the relative std is smaller than 5%, copy the computed average values and paste into https://docs.google.com/spreadsheets/d/108u91potKYYNa4C_enAvwOuuOcTBwIL1ui_K8Cq1bUU/edit#gid=380424475
</li>
</ol>