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

8. Install vmtouch

```
cd ~
git clone https://github.com/hoytech/vmtouch.git
cd vmtouch
make
sudo make install
```

9. Download dataset

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

10. Group the data

```
python group-needle.py /home/cc/data/imagenette2/train/ 2
```
Here 2 is the group size. So we are grouping 2 files into a large `.mytar` file.

11. Train on the grouped data

```
python main-mytar.py -a alexnet --epoch 1 
```