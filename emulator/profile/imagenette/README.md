# Steps

1. Run the command. Example:

`python main-measure-time.py --epoch 1 ~/data/test-accuracy/imagenette2 --gpu 0 --gpu-type p100 -a alexnet --batch-size 256`

Replace the parameters with your gpu-type (p100/v100/rtx6000/...), model type (alexnet/resnet101/...), batch size (256/128/64/...)

2. This will produce a file `p100/alexnet-batch256.csv`.

Open that file, copy the numbers, and paste into the google sheet:

https://docs.google.com/spreadsheets/d/1r2dfwMVD_5S8C_8em-hdN6r_iumH0bj4F2xWZKehUFc/edit#gid=0

The google sheet will compute the average and std of batches 1-10.

Notes:
- You might need to create new rows for a new model. Just follow the style of existing records.

- It ignores batch 0 when computing average and std, because the values from batch 0 are very different from those
from other batches. But please still copy paste batch 0's numbers into the google sheet as a record.

- Sometimes the batch's memory requirement is too large to fit into GPU memory, and you'll see an error like `RuntimeError: CUDA out of memory. Tried to allocate 98.00 MiB (GPU 0; 15.90 GiB total capacity; 14.96 GiB already allocated; 33.75 MiB free; 15.16 GiB reserved in total by PyTorch)`.  When this happens, just put "N/A" in the google sheets. You'll need to reduce the batch size in order to reduce the memory requirement.

- If the computed relative std is larger than 5%, please mark it using bold and red color in the google sheet.

3. If the relative std is smaller than 5%, copy the computed average values and paste into https://docs.google.com/spreadsheets/d/108u91potKYYNa4C_enAvwOuuOcTBwIL1ui_K8Cq1bUU/edit#gid=380424475