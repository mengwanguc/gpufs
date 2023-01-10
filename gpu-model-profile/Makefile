batch64:
	python main-original.py --epoch 1 --gpu=0 -b 64 -a alexnet ~/data/imagenette2 || true
	python main-original.py --epoch 1 --gpu=0 -b 64 -a densenet121 ~/data/imagenette2 || true
	python main-original.py --epoch 1 --gpu=0 -b 64 -a densenet161 ~/data/imagenette2 || true
	python main-original.py --epoch 1 --gpu=0 -b 64 -a densenet169 ~/data/imagenette2 || true
	python main-original.py --epoch 1 --gpu=0 -b 64 -a densenet201 ~/data/imagenette2 || true
	python main-original.py --epoch 1 --gpu=0 -b 64 -a resnet101 ~/data/imagenette2 || true
	python main-original.py --epoch 1 --gpu=0 -b 64 -a resnet152 ~/data/imagenette2 || true
	python main-original.py --epoch 1 --gpu=0 -b 64 -a resnet18 ~/data/imagenette2 || true
	python main-original.py --epoch 1 --gpu=0 -b 64 -a resnet34 ~/data/imagenette2 || true
	python main-original.py --epoch 1 --gpu=0 -b 64 -a resnet50 ~/data/imagenette2 || true
	python main-original.py --epoch 1 --gpu=0 -b 64 -a squeezenet1_0 ~/data/imagenette2 || true
	python main-original.py --epoch 1 --gpu=0 -b 64 -a squeezenet1_1 ~/data/imagenette2 || true
	python main-original.py --epoch 1 --gpu=0 -b 64 -a vgg11 ~/data/imagenette2 || true
	python main-original.py --epoch 1 --gpu=0 -b 64 -a vgg11_bn ~/data/imagenette2 || true
	python main-original.py --epoch 1 --gpu=0 -b 64 -a vgg13 ~/data/imagenette2 || true
	python main-original.py --epoch 1 --gpu=0 -b 64 -a vgg13_bn ~/data/imagenette2 || true
	python main-original.py --epoch 1 --gpu=0 -b 64 -a vgg16 ~/data/imagenette2 || true
	python main-original.py --epoch 1 --gpu=0 -b 64 -a vgg16_bn ~/data/imagenette2 || true
	python main-original.py --epoch 1 --gpu=0 -b 64 -a vgg19 ~/data/imagenette2 || true
	python main-original.py --epoch 1 --gpu=0 -b 64 -a vgg19_bn ~/data/imagenette2 || true
	
batch128:
	python main-original.py --epoch 1 --gpu=0 -b 128 -a alexnet ~/data/imagenette2 || true
	python main-original.py --epoch 1 --gpu=0 -b 128 -a densenet121 ~/data/imagenette2 || true
	python main-original.py --epoch 1 --gpu=0 -b 128 -a densenet161 ~/data/imagenette2 || true
	python main-original.py --epoch 1 --gpu=0 -b 128 -a densenet169 ~/data/imagenette2 || true
	python main-original.py --epoch 1 --gpu=0 -b 128 -a densenet201 ~/data/imagenette2 || true
	python main-original.py --epoch 1 --gpu=0 -b 128 -a resnet101 ~/data/imagenette2 || true
	python main-original.py --epoch 1 --gpu=0 -b 128 -a resnet152 ~/data/imagenette2 || true
	python main-original.py --epoch 1 --gpu=0 -b 128 -a resnet18 ~/data/imagenette2 || true
	python main-original.py --epoch 1 --gpu=0 -b 128 -a resnet34 ~/data/imagenette2 || true
	python main-original.py --epoch 1 --gpu=0 -b 128 -a resnet50 ~/data/imagenette2 || true
	python main-original.py --epoch 1 --gpu=0 -b 128 -a squeezenet1_0 ~/data/imagenette2 || true
	python main-original.py --epoch 1 --gpu=0 -b 128 -a squeezenet1_1 ~/data/imagenette2 || true
	python main-original.py --epoch 1 --gpu=0 -b 128 -a vgg11 ~/data/imagenette2 || true
	python main-original.py --epoch 1 --gpu=0 -b 128 -a vgg11_bn ~/data/imagenette2 || true
	python main-original.py --epoch 1 --gpu=0 -b 128 -a vgg13 ~/data/imagenette2 || true
	python main-original.py --epoch 1 --gpu=0 -b 128 -a vgg13_bn ~/data/imagenette2 || true
	python main-original.py --epoch 1 --gpu=0 -b 128 -a vgg16 ~/data/imagenette2 || true
	python main-original.py --epoch 1 --gpu=0 -b 128 -a vgg16_bn ~/data/imagenette2 || true
	python main-original.py --epoch 1 --gpu=0 -b 128 -a vgg19 ~/data/imagenette2 || true
	python main-original.py --epoch 1 --gpu=0 -b 128 -a vgg19_bn ~/data/imagenette2 || true
	
installer:
	wget https://repo.anaconda.com/archive/Anaconda3-2021.11-Linux-x86_64.sh
	bash Anaconda3-2021.11-Linux-x86_64.sh
	conda install -y astunparse numpy ninja pyyaml mkl mkl-include setuptools cmake cffi typing_extensions future six requests dataclasses
	cd ~
	git clone git@github.com:mengwanguc/pytorch-meng.git
	cd pytorch-meng
	git submodule update --init --recursive
	export CMAKE_PREFIX_PATH=${CONDA_PREFIX:-"$(dirname $(which conda))/../"}
	python setup.py install
	conda install -y aiofiles
	cd ~
	git clone git@github.com:mengwanguc/torchvision-meng.git
	cd torchvision-meng/
	python setup.py install
	cd ~
	git clone https://github.com/hoytech/vmtouch.git
	cd vmtouch
	make
	sudo make install
	cd ~
	mkdir data
	cd data
	pip install gdown
	gdown https://drive.google.com/uc?id=1ywwFMZRZEdoEkvTD-Q_AGW0w-FU3-6gw
	tar -zxf imagenette2.tar.gz
	cd ~/gpufs/grouping
	python group-needle.py /home/cc/data/imagenette2/train/ 2 /home/cc/data/mytar
	cd ~/gpufs/exp
	python main-mytar.py -a alexnet --epoch 1 --img_per_tar 2
	python main-original.py --epoch 1 -a alexnet ~/data/imagenette2
	cd ~
	mkdir data
	cd data
	mkdir test-accuracy
	cd test-accuracy
	wget https://s3.amazonaws.com/fast-ai-imageclas/imagenette2.tgz
	tar -zxvf imagenette2.tgz
	cd ~/gpufs/grouping
	python group-needle.py ~/data/test-accuracy/imagenette2/train 4 ~/data/test-accuracy/mytar/train
	cd ~/gpufs/exp
	python main-group-accuracy.py ~/data/test-accuracy/mytar/train/4/ ~/data/test-accuracy/imagenette2/val/ --img_per_tar 4

run: batch64 batch128 installer

.PHONY: run batch64 batch128 installer
