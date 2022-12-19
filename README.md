# gpufs

## Installation

1. Set up ssh
```
ssh-keygen -t rsa -b 4096
ssh-keyscan -t rsa github.com >> ~/.ssh/known_hosts
cat ~/.ssh/id_rsa.pub
```

Copy and paste into: https://github.com/settings/keys

2. clone this repo to local

```
git clone git@github.com:mengwanguc/gpufs.git
```

3. Install conda

```
wget https://repo.anaconda.com/archive/Anaconda3-2021.11-Linux-x86_64.sh
bash Anaconda3-2021.11-Linux-x86_64.sh
```
After installation, log out and log in bash again.

4. Install packages required for builing pytorch

**Note: the commands below assumes you have cuda 10.2 installed on your machine. If you have other cuda versions, please use the magma-cuda\* that matches your CUDA version from** https://anaconda.org/pytorch/repo.

For example, if your cuda version is 11.2 (check it by running nvidia-smi), then the command should be `conda install -y -c pytorch magma-cuda112`

```
conda install -y astunparse numpy ninja pyyaml mkl mkl-include setuptools cmake cffi typing_extensions future six requests dataclasses

# CUDA only: Add LAPACK support for the GPU if needed
conda install -y -c pytorch magma-cuda102  # or the magma-cuda* that matches your CUDA version from https://anaconda.org/pytorch/repo
```

5. Install gcc 7
```
sudo yum install -y centos-release-scl
sudo yum install -y devtoolset-7
scl enable devtoolset-7 bash
```

6. Download our custom pytorch and build it

**NOTE: our custom pytorch assumes that you are using cuda 10.2. If you are using cuda 11, please install the original pytorch from** https://github.com/pytorch/pytorch#installation

```
cd ~
git clone git@github.com:mengwanguc/pytorch-meng.git
cd pytorch-meng
git submodule update --init --recursive

export CMAKE_PREFIX_PATH=${CONDA_PREFIX:-"$(dirname $(which conda))/../"}
python setup.py install
```

7. Download our custom torchvision and build it

```
conda install -y aiofiles

cd ~
git clone git@github.com:mengwanguc/torchvision-meng.git
cd torchvision-meng/
python setup.py install
```


## See effect of grouping on gpu utilization:

** If you only care about accuracy, please go to ["Training Accuracy"](#training-accuracy). **

1. Install vmtouch

```
cd ~
git clone https://github.com/hoytech/vmtouch.git
cd vmtouch
make
sudo make install
```

2. Download dataset

```
cd ~
mkdir data
cd data
pip install gdown
gdown https://drive.google.com/uc?id=1ywwFMZRZEdoEkvTD-Q_AGW0w-FU3-6gw
tar -zxf imagenette2.tar.gz
```
Note: this is NOT the original Imagenette dataset. I produced the dataset based on Imagenette dataset by copying its files/folders again and again to reach 10G data size.

DON'T train accuracy using this file.
ONLY perform dummy tests using this file to evaluate GPU utilization.

If you want to train accuracy on Imagenette dataset, please see: https://github.com/fastai/imagenette

3. Group the data

```
cd ~/gpufs/grouping
python group-needle.py /home/cc/data/imagenette2/train/ 2 /home/cc/data/mytar
```
Here 2 is the group size. So we are grouping 2 files into a large `.mytar` file.

4. Train on the grouped data

```
cd ~/gpufs/exp
python main-mytar.py -a alexnet --epoch 1 --img_per_tar 2
```
This will train based on group size 2.

```
python main-original.py --epoch 1 -a alexnet ~/data/imagenette2
```
This will train using the original pytorch and script.

## Training accuracy

As an example, let's start with Imagenette:

1. First, download the [imagenettee](https://github.com/fastai/imagenette) dataset:

```
cd ~
mkdir data
cd data
mkdir test-accuracy
cd test-accuracy
wget https://s3.amazonaws.com/fast-ai-imageclas/imagenette2.tgz
tar -zxvf imagenette2.tgz
```

2. Group it:

```
cd ~/gpufs/grouping
python group-needle.py ~/data/test-accuracy/imagenette2/train 4 ~/data/test-accuracy/mytar/train
```

This will group the training data into groups of size 4, and stored in `~/data/test-accuracy/mytar/train/4/`.

3. Train it:

example:


```
cd ~/gpufs/exp
python main-group-accuracy.py ~/data/test-accuracy/mytar/train/4/ ~/data/test-accuracy/imagenette2/val/ --img_per_tar 4
```

Usage:

```
usage: main-group-accuracy.py [-h] [-a ARCH] [-j N] [--epochs N] [--start-epoch N] [-b N] [--lr LR] [--momentum M] [--wd W] [-p N] [--resume PATH] [-e] [--pretrained]
                              [--world-size WORLD_SIZE] [--rank RANK] [--dist-url DIST_URL] [--dist-backend DIST_BACKEND] [--seed SEED] [--gpu GPU]
                              [--multiprocessing-distributed] [--img_per_tar IMG_PER_TAR] [--is_async IS_ASYNC]
                              TRAIN_DIR VALIDATE_DIR

```
Here `TRAIN_DIR` is the folder that stores the grouped training data. `VALIDATE_DIR` is the folder that stores UNgrouped validation data.

An example output look like this:

```
(base) python main-group-accuracy.py ~/data/test-accuracy/mytar/train/4/ ~/data/test-accuracy/imagenette2/val/ --img_per_tar 4
args.img_per_tar: 4
args.is_async: 0
img_per_tar:  4
is_async:  0
=> creating model 'resnet18'
{'n01440764': 0, 'n02102040': 1, 'n02979186': 2, 'n03000684': 3, 'n03028079': 4, 'n03394916': 5, 'n03417042': 6, 'n03425413': 7, 'n03445777': 8, 'n03888257': 9}
{'n01440764': 0, 'n02102040': 1, 'n02979186': 2, 'n03000684': 3, 'n03028079': 4, 'n03394916': 5, 'n03417042': 6, 'n03425413': 7, 'n03445777': 8, 'n03888257': 9}
using tar format!
grouping using my own tar format!
using random sampler...

Epoch: [0][ 0/37]       Time  6.057 ( 6.057)    Data  2.280 ( 2.280)    Loss 7.1222e+00 (7.1222e+00)    Acc@1   0.00 (  0.00)   Acc@5   0.00 (  0.00)
Epoch: [0][10/37]       Time  0.861 ( 1.332)    Data  0.000 ( 0.211)    Loss 1.2117e+01 (6.5338e+00)    Acc@1  10.16 ( 12.78)   Acc@5  48.83 ( 47.37)
Epoch: [0][20/37]       Time  0.861 ( 1.108)    Data  0.000 ( 0.114)    Loss 5.9464e+00 (7.2883e+00)    Acc@1  12.89 ( 12.20)   Acc@5  54.30 ( 49.59)
Epoch: [0][30/37]       Time  0.863 ( 1.028)    Data  0.000 ( 0.079)    Loss 3.1204e+00 (6.1865e+00)    Acc@1  10.55 ( 12.10)   Acc@5  53.12 ( 50.16)
Test: [ 0/16]   Time  2.730 ( 2.730)    Loss 2.1307e+01 (2.1307e+01)    Acc@1   0.00 (  0.00)   Acc@5  69.92 ( 69.92)
Test: [10/16]   Time  0.303 ( 0.735)    Loss 5.3007e+01 (4.3082e+01)    Acc@1   2.73 (  8.10)   Acc@5  62.11 ( 52.95)
 * Acc@1 7.567 Acc@5 48.611
using random sampler...

Epoch: [1][ 0/37]       Time  3.094 ( 3.094)    Data  2.288 ( 2.288)    Loss 2.8809e+00 (2.8809e+00)    Acc@1  12.89 ( 12.89)   Acc@5  55.47 ( 55.47)
Epoch: [1][10/37]       Time  0.860 ( 1.065)    Data  0.000 ( 0.214)    Loss 2.4721e+00 (2.5114e+00)    Acc@1  12.50 ( 13.21)   Acc@5  57.42 ( 57.10)
Epoch: [1][20/37]       Time  0.861 ( 0.968)    Data  0.000 ( 0.116)    Loss 2.3135e+00 (2.4293e+00)    Acc@1  13.28 ( 14.23)   Acc@5  62.50 ( 58.37)
Epoch: [1][30/37]       Time  0.861 ( 0.934)    Data  0.000 ( 0.080)    Loss 2.4373e+00 (2.4020e+00)    Acc@1  19.92 ( 15.88)   Acc@5  61.33 ( 59.84)
Test: [ 0/16]   Time  2.776 ( 2.776)    Loss 2.3261e+00 (2.3261e+00)    Acc@1   0.00 (  0.00)   Acc@5  71.88 ( 71.88)
Test: [10/16]   Time  0.433 ( 0.726)    Loss 2.2573e+00 (2.2985e+00)    Acc@1  19.92 ( 14.20)   Acc@5  53.52 ( 65.20)
 * Acc@1 18.344 Acc@5 65.529
using random sampler...

Epoch: [2][ 0/37]       Time  2.941 ( 2.941)    Data  2.123 ( 2.123)    Loss 2.2315e+00 (2.2315e+00)    Acc@1  15.62 ( 15.62)   Acc@5  63.67 ( 63.67)
Epoch: [2][10/37]       Time  0.860 ( 1.051)    Data  0.000 ( 0.199)    Loss 2.1777e+00 (2.2078e+00)    Acc@1  23.44 ( 19.85)   Acc@5  62.11 ( 62.93)
Epoch: [2][20/37]       Time  0.861 ( 0.961)    Data  0.000 ( 0.108)    Loss 2.1109e+00 (2.1903e+00)    Acc@1  23.83 ( 20.68)   Acc@5  66.41 ( 63.93)
Epoch: [2][30/37]       Time  0.860 ( 0.929)    Data  0.000 ( 0.075)    Loss 2.2324e+00 (2.1872e+00)    Acc@1  21.09 ( 20.93)   Acc@5  62.50 ( 64.67)
Test: [ 0/16]   Time  2.735 ( 2.735)    Loss 2.1135e+00 (2.1135e+00)    Acc@1  40.23 ( 40.23)   Acc@5  85.55 ( 85.55)
Test: [10/16]   Time  0.303 ( 0.723)    Loss 1.8741e+00 (2.1837e+00)    Acc@1  36.72 ( 19.03)   Acc@5  97.27 ( 66.90)
 * Acc@1 21.554 Acc@5 68.025
```


