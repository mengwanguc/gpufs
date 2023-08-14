#!/bin/bash

echo "Start running"
python main-measure-time.py -a alexnet -j 4 --epochs 1 -b 128 ~/data/test-accuracy/imagenette2 &> output_alexnet_128.txt
echo "finished 1"
python main-measure-time.py -a alexnet -j 4 --epochs 1 -b 256 ~/data/test-accuracy/imagenette2 &> output_alexnet_256.txt
echo "finished 2"
python main-measure-time.py -a alexnet -j 4 --epochs 1 -b 512 ~/data/test-accuracy/imagenette2 &> output_alexnet_512.txt
echo "finished 3"
python main-measure-time.py -a alexnet -j 4 --epochs 1 -b 1024 ~/data/test-accuracy/imagenette2 &> output_alexnet_1024.txt
echo "finished 4"