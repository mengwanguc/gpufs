#!/bin/bash

benchmark(){
	lr=$1
	epoch=$2
	for weight_decay in 0.0001 0.001 0.01 0.1 0
	do
        for eps in 0.01 0.001 0.0001
        do
        echo "$lr $epoch $weight_decay $eps"
        python main-original-adam.py -a resnet18 --lr $lr ~/data/ILSVRC/Data/CLS-LOC --epochs $epoch --eps $eps --weight_decay $weight_decay
        ./
        done
	done

}

benchmark 0.1 5
