## Installation on CPU-only node

#### Note: the commands below should be run on your reserved Chameleon node connected through ssh, not your local laptop.

1. Chameleon image

Please use image "ubuntu20-xxx."

"xxx" means we don't care about what's there, as long as it's using ubuntu20.

Successful tests:
- TACC "zen3" node, image "CC-Ubuntu20.04". Tested by Meng (May 28 2023)
- "xxx" node, image "xxx". Tested by xxx (time xxx)

2. Set up ssh
```
ssh-keygen -t rsa -b 4096
ssh-keyscan -t rsa github.com >> ~/.ssh/known_hosts
cat ~/.ssh/id_rsa.pub
```

Copy and paste into: https://github.com/settings/keys

3. clone this repo to local

```
git clone git@github.com:mengwanguc/gpufs.git
```

4. Install conda

```
wget https://repo.anaconda.com/archive/Anaconda3-2021.11-Linux-x86_64.sh
bash Anaconda3-2021.11-Linux-x86_64.sh
```

When it prompts to ask "yes|no", always put "yes".

After installation, log out the terminal (just close terminal) and log in again. You should see your terminal outputs:

```
(base) cc@ubuntu:~/
```


5. Install packages required for builing pytorch

```
conda install -y astunparse numpy ninja pyyaml mkl mkl-include setuptools cmake cffi typing_extensions future six requests dataclasses
```


6. Download and build mlock (which can allocate page-locked memory)

cd ~
git clone git@github.com:gustrain/mlock.git
cd mlock
python setup.py install

7. Download and build minio

cd ~
git clone git@github.com:gustrain/minio.git
cd minio
python setup.py install




8. Download our custom pytorch and build it (Note that we use "export USE_CUDA=0" to not install any cuda/GPU-related things.)

```
cd ~
git clone git@github.com:mengwanguc/pytorch-meng.git
cd pytorch-meng
git submodule update --init --recursive

export CMAKE_PREFIX_PATH=${CONDA_PREFIX:-"$(dirname $(which conda))/../"}
export USE_CUDA=0
python setup.py install
```

9. Download our custom torchvision and build it

```
conda install -y aiofiles

cd ~
git clone git@github.com:mengwanguc/torchvision-meng.git
cd torchvision-meng/
python setup.py install
```

10. Update `/etc/security/limits.conf`

```
sudo nano /etc/security/limits.conf
```

Add the following text to the end of the file:

```
*   soft    memlock     unlimited
*   hard    memlock     unlimited
```

11. Reboot the machine

```
sudo reboot
```




