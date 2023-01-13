#!/bin/bash

benchmark(){
	batchsize=$1
	epochsize=$2
	for groupsize in {1,2,4,8,16,32,64}
	do
	python imagenette2/main-group-accuracy.py ~/data/test-accuracy/mytar/train2/$groupsize/ ~/data/test-accuracy/imagenette2/val/ --img_per_tar $groupsize --epoch $epochsize -a resnet101 -b $batchsize
	python imagenette3/main-group-accuracy.py ~/data/test-accuracy/mytar/train3/$groupsize/ ~/data/test-accuracy/imagenette2/val/ --img_per_tar $groupsize --epoch $epochsize -a resnet101 -b $batchsize 
	python imagenette4/main-group-accuracy.py ~/data/test-accuracy/mytar/train4/$groupsize/ ~/data/test-accuracy/imagenette2/val/ --img_per_tar $groupsize --epoch $epochsize -a resnet101 -b $batchsize
	python imagenette5/main-group-accuracy.py ~/data/test-accuracy/mytar/train5/$groupsize/ ~/data/test-accuracy/imagenette2/val/ --img_per_tar $groupsize --epoch $epochsize -a resnet101 -b $batchsize
	./
	done

}

benchmark 128 50
