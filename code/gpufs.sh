#!/bin/bash

benchmark(){
	groupsize=$1
	epochsize=$2
	for batchsize in {64,128,256}
	do
	python main-group-accuracy.py ~/data/test-accuracy/mytar/train/$groupsize/ ~/data/test-accuracy/imagenette2/val/ --img_per_tar $groupsize --epoch $epochsize -a alexnet -b $batchsize 
	python main-group-accuracy.py ~/data/test-accuracy/mytar/train/$groupsize/ ~/data/test-accuracy/imagenette2/val/ --img_per_tar $groupsize --epoch $epochsize -a resnet18 -b $batchsize 
	python main-group-accuracy.py ~/data/test-accuracy/mytar/train/$groupsize/ ~/data/test-accuracy/imagenette2/val/ --img_per_tar $groupsize --epoch $epochsize -a resnet101 -b $batchsize 
	python main-group-accuracy.py ~/data/test-accuracy/mytar/train/$groupsize/ ~/data/test-accuracy/imagenette2/val/ --img_per_tar $groupsize --epoch $epochsize -a vgg11 -b $batchsize 
	./
	done

}

benchmark 1 50
benchmark 2 50
benchmark 4 50
benchmark 8 50
benchmark 16 50
benchmark 32 50
benchmark 64 50
