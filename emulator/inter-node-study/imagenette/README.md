python main-original.py --dist-url 'tcp://10.140.81.208:12345' --dist-backend 'nccl' --multiprocessing-distributed --world-size 2 --rank 0 ~/data/test-accuracy/imagenette2/

python main-original.py --dist-url 'tcp://10.140.81.208:12345' --dist-backend 'nccl' --multiprocessing-distributed --world-size 2 --rank 1 ~/data/test-accuracy/imagenette2


