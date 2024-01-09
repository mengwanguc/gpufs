## Measuring Preprocessing Time for DALI

1. Install all depedencies

   To install gpufs contained ffcv folder. and others depedencies.
    
   Need doing all step on https://github.com/mengwanguc/gpufs#readme until you done clone gpufs repository.

   And move to naufal branch:
   ```
   git checkout naufal
   ```

   Install the env with this, it will created ffcv env:
   ```
    conda create -n ffcv python=3.9 cupy pkg-config libjpeg-turbo opencv pytorch torchvision cudatoolkit=11.6 numba -c conda-forge -c pytorch && conda activate ffcv && conda update ffmpeg && pip install ffcv
                    
   ```

    Using ffcv env, Install Dali in Ubuntu:
    ```
    pip install nvidia-dali-cuda110
    ```

2. Copying __init__.py into dali folder
    this file will load a pickle file used for dummy data to prevent preprocessing getting problem.
    
    ```
    /home/cc/gpufs/nvidia-dali/__init__(custom).py
    ```
    replaced this script into 
    ```
    /home/cc/anaconda3/envs/ffcv/lib/python3.9/site-packages/nvidia/dali/plugin/pytorch/__init__.py (depend on your dali folder path)
    ```

    ```
    cp /home/cc/gpufs/nvidia-dali/__init__.py /home/cc/anaconda3/envs/ffcv/lib/python3.9/site-packages/nvidia/dali/plugin/pytorch/__init__.py
    ```
    

3. Training a model.
    This command will trained the model using small imagenet dataset (contained 16 images) with batch size 16. It will created preprocessing-time-images16-bsize16-all.txt.
    you can change --exp_name for name your file. 
    ```
    python main-nvidia-dali-gpu.py dataset/small-imagenet-16/ -b 16 --exp_name images16-bsize16-all
    ```

3. Measuring Preprocessing Time.
    In create_dali_pipeline() you will see 4 step of preprocessing data on dali. To measure them you can comment other code. For example you want to measure reader step, you should comment other step like decoder, resize, and normalize. Another example if you want to measure decoder you have to comment resize and normalize. And so on for others.

   


```
python main-nvidia-dali-gpu.py dataset/small-imagenet-16/ -b 16 --exp_name images16-bsize16-all --epochs 1 --deterministic
python main-nvidia-dali-gpu.py dataset/small-imagenet-16/ -b 4 --exp_name images16-bsize16-all --epochs 1 --deterministic

```

## Usage

```
usage: main-nvidia-dali-gpu.py [-h] [--arch ARCH] [-j N] [--epochs N] [--start-epoch N] [-b N] [--lr LR] [--momentum M] [--weight-decay W]
                               [--print-freq N] [--resume PATH] [-e] [--pretrained] [--dali_cpu] [--disable_dali] [--prof PROF] [--deterministic]
                               [--fp16-mode] [--loss-scale LOSS_SCALE] [--channels-last CHANNELS_LAST] [-t] [--exp_name EXP_NAME]
                               [DIR ...]

PyTorch ImageNet Training

positional arguments:
  DIR                   path(s) to dataset (if one path is provided, it is assumed to have subdirectories named "train" and "val"; alternatively,
                        train and val paths can be specified directly by providing both paths as arguments)

optional arguments:
  -h, --help            show this help message and exit
  --arch ARCH, -a ARCH  model architecture: alexnet | convnext_base | convnext_large | convnext_small | convnext_tiny | densenet121 | densenet161
                        | densenet169 | densenet201 | efficientnet_b0 | efficientnet_b1 | efficientnet_b2 | efficientnet_b3 | efficientnet_b4 |
                        efficientnet_b5 | efficientnet_b6 | efficientnet_b7 | efficientnet_v2_l | efficientnet_v2_m | efficientnet_v2_s |
                        get_model | get_model_builder | get_model_weights | get_weight | googlenet | inception_v3 | list_models | maxvit_t |
                        mnasnet0_5 | mnasnet0_75 | mnasnet1_0 | mnasnet1_3 | mobilenet_v2 | mobilenet_v3_large | mobilenet_v3_small |
                        regnet_x_16gf | regnet_x_1_6gf | regnet_x_32gf | regnet_x_3_2gf | regnet_x_400mf | regnet_x_800mf | regnet_x_8gf |
                        regnet_y_128gf | regnet_y_16gf | regnet_y_1_6gf | regnet_y_32gf | regnet_y_3_2gf | regnet_y_400mf | regnet_y_800mf |
                        regnet_y_8gf | resnet101 | resnet152 | resnet18 | resnet34 | resnet50 | resnext101_32x8d | resnext101_64x4d |
                        resnext50_32x4d | shufflenet_v2_x0_5 | shufflenet_v2_x1_0 | shufflenet_v2_x1_5 | shufflenet_v2_x2_0 | squeezenet1_0 |
                        squeezenet1_1 | swin_b | swin_s | swin_t | swin_v2_b | swin_v2_s | swin_v2_t | vgg11 | vgg11_bn | vgg13 | vgg13_bn | vgg16
                        | vgg16_bn | vgg19 | vgg19_bn | vit_b_16 | vit_b_32 | vit_h_14 | vit_l_16 | vit_l_32 | wide_resnet101_2 | wide_resnet50_2
                        (default: resnet18)
  -j N, --workers N     number of data loading workers (default: 4)
  --epochs N            number of total epochs to run
  --start-epoch N       manual epoch number (useful on restarts)
  -b N, --batch-size N  mini-batch size per process (default: 256)
  --lr LR, --learning-rate LR
                        Initial learning rate. Will be scaled by <global batch size>/256: args.lr =
                        args.lr*float(args.batch_size*args.world_size)/256. A warmup schedule will also be applied over the first 5 epochs.
  --momentum M          momentum
  --weight-decay W, --wd W
                        weight decay (default: 1e-4)
  --print-freq N, -p N  print frequency (default: 10)
  --resume PATH         path to latest checkpoint (default: none)
  -e, --evaluate        evaluate model on validation set
  --pretrained          use pre-trained model
  --dali_cpu            Runs CPU based version of DALI pipeline.
  --disable_dali        Disable DALI data loader and use native PyTorch one instead.
  --prof PROF           Only run 10 iterations for profiling.
  --deterministic
  --fp16-mode           Enable half precision mode.
  --loss-scale LOSS_SCALE
  --channels-last CHANNELS_LAST
  -t, --test            Launch test mode with preset arguments
  --exp_name EXP_NAME   named preprocessing time txt
```
