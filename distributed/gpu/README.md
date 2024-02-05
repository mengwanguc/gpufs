export GLOO_SOCKET_IFNAME=eno1

python main.py -a resnet50 --dist-url 'tcp://10.140.83.62:55555' --dist-backend 'gloo' --multiprocessing-distributed --world-size 2 --rank 0 /home/cc/data/test-accuracy/imagenette2

python main.py -a resnet50 --dist-url 'tcp://10.140.83.62:55555' --dist-backend 'gloo' --multiprocessing-distributed --world-size 2 --rank 1 /home/cc/data/test-accuracy/imagenette2