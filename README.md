- wenbo folder: data & graphs

`Folders:`
base_model_data: data generated from baseline model
base_model_graph: graphs generated from baseline model data

grouped_model_data: data generated from different group sizes
grouped_model_graph: graphs generated from different group sizes

outdated_prefix folder means that we used it in previous experiment, but it is not effective somehow.

Resnet_bs128 & resnet_bs128_graph: generated data and graphs by the same permutation number.


`The structure of JSON file (dictionary)`:
{
	"train_top1": []   #list of acc
	"train_top5": []
	"val_top1": []
	"val_top5": []
	"model": "alexnet"
	"args.epoch": 50      
	"args.batch_sizes": 64/128/256
	"batch_acc_train": {"100": [], "200":[],...} # calculated data per 100 batches
	"batch_acc_val": {"100": [], "200":[],...}
}

`Plotting`:
`read_and_plot.py` takes inputs from the JSON files in the data folder and plot graphs to the graph folder; loop through each elements in the JSON files and draw the graph.

`read_and_plot_grouped.py` same as the `read_and_plot.py` but edited for better usage for different group sizes



- code folder: bash script and edited main-group-accuracy.py & main-original.py


- `grouping folder`: 

`gen-perms.py`: generate random permutation seeds and write it to the perms folder
perms subfolder: stores each single seed as seed1.txt

`group-needle.py`: edited line 107 to line 113 to take the same seed;


-------------Example---------------
1. `cd ~/gpufs/grouping`
2. `python gen-perms.py` # generate seed from gen-perms.py and store `seed1.txt` to perms folder, or we can just simply use the generated seeds in the perms folder
3. `python group-needle.py ~/data/test-accuracy/imagenette2/train 4 ~/data/test-accuracy/mytar/train` # we can run through each group size using `bash group.sh`
4. `cd ~/gpufs/exp`
5. `bash gpufs.sh` #edit groupsize, epochsize, batchsize, and add/comment_out models
by the default of `main-group-accuracy.py` line 336, the generated data will output to the current folder; edit it if needed
6. `cd ~/gpufs/exp/wenbo`
7.  After getting all the data in the new data folder such as `grouped_model_data`, we can draw the graph using
python `read_and_plot_grouped.py` #rememebr to edit line 24-27 to change title and dictionary key, and save the figures on line 127-129; please refer to the above JSON file structures


