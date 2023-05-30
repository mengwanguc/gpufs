# README FIRST before doing experiments!!!

## NOTES

- When you install our custom "pytorch-meng" and "torchvision-meng", please use branches **"original-pytorch"** and **"original-torchvision"** respectively.

- Use "run-all.sh" to save your life when running experiments for a lot of models and batch sizes. See Step 1 to learn how to use it.

- Please README thoroughly!!!

## Summary

1. `bash run-all.sh &> output.log` using `tmux`

2. `python parse-profiles.py p100`. Replace `p100` with your own GPU type

3. Copy from `p100/all.txt` (or your own gpu type) and paste into google sheets

## Detailed steps
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

**NOTE**: 
- I suggest you use `tmux` to run `run-all.sh` in the background. If you don't want what's `tmux` and how to use it, Google it. 

- I also recommend you save the output into a file. For example, `bash run-all.sh &> output.log`. Don't commit this log file, but this file will be great for debugging purpose.

- By using `tmux`, you don't have to keep your terminal open and connected when running the experiments. You can let the experiments run in the background, close the terminal, do something else, and come back after hours to check the results. Again if you don't know how to use `tmux`, google it. I believe it will be useful for your future work as well.

</li>

</ul>
</li>



<li>
In 

https://docs.google.com/spreadsheets/d/1r2dfwMVD_5S8C_8em-hdN6r_iumH0bj4F2xWZKehUFc/edit#gid=0

make a duplicate of the sheet "p100 (Meng)" and rename it to your own gpu type and name. Delete the existing values for batch 0-10 for all the models and batch sizes. BUT don't delete average/std/relative-std because these cells are formulas.
</li>

<li>
Open the file in e.g. `p100/` folder, e.g. `p100/alexnet-batch256.csv`, copy the **numbers**, and paste into the google sheet.

The google sheet will compute the average and std of batches 1-10.

To reduce the number of copy-pastes, I created `parse-profiles.py`.

For example, after generating all the profiles using `run-all.sh`, you can run:

`python parse-profiles.py p100`

This will parse all the generated profiles, gather them, and produce a summary file `p100/all.txt`. Open that file and you'll see what I mean.
Now you can copy paste into google sheets more easily.

(You'll need to replace `p100` with your own gpu type)

**Notes:**

- It ignores batch 0 when computing average and std, because the values from batch 0 are very different from those
from other batches. But please still copy paste batch 0's numbers into the google sheet as a record.

- Sometimes the batch's memory requirement is too large to fit into GPU memory, and you'll see an error like `RuntimeError: CUDA out of memory. Tried to allocate 98.00 MiB (GPU 0; 15.90 GiB total capacity; 14.96 GiB already allocated; 33.75 MiB free; 15.16 GiB reserved in total by PyTorch)`.  When this happens, just put "N/A" in the google sheets. You'll need to reduce the batch size in order to reduce the memory requirement.

- If you are using `run-all.sh`, and see some `.csv` files are missing, that is probably caused by the `out of memory` error as mentioned above. So just go ahead check your output log file generated in step 1, e.g. `output.log`, and search for the model and batch size. If you see the `out of memory` error, then put `N/A`.

- If the computed relative std is larger than 5%, please mark it using **bold and red color** in the google sheet.

</li>

<li>
Scroll down to the bottom of the sheet. You just see there are rows automatically gather all the average values. Copy the computed average values and paste into https://docs.google.com/spreadsheets/d/108u91potKYYNa4C_enAvwOuuOcTBwIL1ui_K8Cq1bUU/edit#gid=380424475

(You might need to create a new sheet)
</li>
</ol>