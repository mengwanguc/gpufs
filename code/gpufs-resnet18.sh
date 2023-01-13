#!/bin/bash

benchmark(){
	batchsize=$1
	epochsize=$2
	for groupsize in {1,2,4,8,16,32,64}
	do
	python main-group-accuracy.py ~/data/test-accuracy/mytar/train2/$groupsize/ ~/data/test-accuracy/imagenette2/val/ --img_per_tar $groupsize --epoch $epochsize -a resnet18 -b $batchsize 
	./
	done

}

benchmark 128 50
