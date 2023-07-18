# Object detection reference training scripts

## Installation the setup

1. Install all depedencies

   To install gpufs(detection files), pytorch, and torchvision
    
   Need doing all step on https://github.com/mengwanguc/gpufs#readme until torchvision installed

   And move to naufal branch:
   ```
   git checkout naufal
   ```

   Install depedencies that we need:
   ```
    pip install gdown
    pip install unzip
    pip install pycocotools
    pip install cython
   ```

3. Install mini-coco dataset (that contain ~20% original coco dataset)

   Note: Run this one by one per lines because when you installed using gdown it needs to press enter if theres no progress download bar.
   
   ```
   cd ~
   mkdir mini-coco-dataset
   cd mini-coco-dataset
   gdown https://drive.google.com/uc?id=1FZiAiws85BqI_LScbNX1cTacl5RyhfTY&export=download
   unzip coco_minitrain_25k_2.zip
   cd coco_minitrain_25k/annotations/
   gdown https://drive.google.com/u/0/uc?id=1lezhgY4M_Ag13w0dEzQ7x_zQ_w0ohjin&export=download
   mv instances_minitrain2017.json instances_train2017.json
   ```
   
4. Using subset of coco dataset (that contain 16 images train and 4 images val) for debugging

   We need to backup the original mini-coco annotation files in cases need in the future

   ```
   cd ~
   cd coco_minitrain_25k/annotations/
   mkdir backup
   mv instances_train2017.json backup/
   mv instances_val2017.json backup/
   ```

   Annotation for the 16 images can be found in gpufs/detection/instances_train2017.json and gpufs/detection/instances_val2017.json

   Need to move it to minitrain folder
   ```
   cd ~
   cd gpufs/detection/
   mv instances_train2017.json ~/coco_minitrain_25k/annotations/
   mv instances_val2017.json ~/coco_minitrain_25k/annotations/  
   ```
   
5. Training the model

   Note: if you have error "Loss function result is NaN", fixing it by change learning rates with formula  0.02/8*$NGPU. Lr depends on how many gpu we are using. And n_workers > 0 will reproduce segmentation fault error
   ```
   cd ~/gpufs/detection/
   python train.py --data-path ~/mini-coco-dataset/coco_minitrain_25k --epoch 2 --lr 0.0025 --workers 0
   ```

   Parameter information:
   ```
   usage: train.py [-h] [--data-path DATA_PATH] [--dataset DATASET] [--model MODEL] [--device DEVICE] [-b BATCH_SIZE] [--epochs N] [-j N] [--lr LR]
                [--momentum M] [--wd W] [--lr-step-size LR_STEP_SIZE] [--lr-steps LR_STEPS [LR_STEPS ...]] [--lr-gamma LR_GAMMA]
                [--print-freq PRINT_FREQ] [--output-dir OUTPUT_DIR] [--resume RESUME] [--start_epoch START_EPOCH]
                [--aspect-ratio-group-factor ASPECT_RATIO_GROUP_FACTOR] [--test-only] [--pretrained] [--world-size WORLD_SIZE] [--dist-url DIST_URL]
   ```
## Using Grouping Method

1. Grouping dataset using group-needle code

   param: python group-needle-detection.py <train_folder> <groupsize> <mytar_save_folder> 
   ```
   cd ~/gpufs/detection
   python group-needle-detection-based-images-annotations.py ~/mini-coco-dataset/coco_minitrain_25k 4 ~/mini-coco-dataset/grouped-data-images-annotations
   ```
2. Training the grouped data
   
   param: python train-grouping.py <grouped_data>
   
   note: --aspect-ratio-group-factor should be -1 because we already using it in group-needle. --workers should 0 to prevent segmentation fault error. --lr depends on how many gpu we are using (0.02/8*$NGPU).
   ```
   cd ~/gpufs/detection
   python train-grouping.py --train_data "/home/cc/mini-coco-dataset/grouped-data-images-annotations-v2-subset/" --epoch 2 --lr 0.0025 --workers 0 --aspect-ratio-group-factor -1 --batch-size 4 --group-size 4
   ```

## Original Readme

This folder contains reference training scripts for object detection.
They serve as a log of how to train specific models, to provide baseline
training and evaluation scripts to quickly bootstrap research.

To execute the example commands below you must install the following:

```
cython
pycocotools
matplotlib
```

You must modify the following flags:

`--data-path=/path/to/coco/dataset`

`--nproc_per_node=<number_of_gpus_available>`

Except otherwise noted, all models have been trained on 8x V100 GPUs. 

### Faster R-CNN
```
python -m torch.distributed.launch --nproc_per_node=8 --use_env train.py\
    --dataset coco --model fasterrcnn_resnet50_fpn --epochs 26\
    --lr-steps 16 22 --aspect-ratio-group-factor 3
```

### RetinaNet
```
python -m torch.distributed.launch --nproc_per_node=8 --use_env train.py\
    --dataset coco --model retinanet_resnet50_fpn --epochs 26\
    --lr-steps 16 22 --aspect-ratio-group-factor 3 --lr 0.01
```


### Mask R-CNN
```
python -m torch.distributed.launch --nproc_per_node=8 --use_env train.py\
    --dataset coco --model maskrcnn_resnet50_fpn --epochs 26\
    --lr-steps 16 22 --aspect-ratio-group-factor 3
```


### Keypoint R-CNN
```
python -m torch.distributed.launch --nproc_per_node=8 --use_env train.py\
    --dataset coco_kp --model keypointrcnn_resnet50_fpn --epochs 46\
    --lr-steps 36 43 --aspect-ratio-group-factor 3
```

