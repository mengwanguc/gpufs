python main-nvidia-dali-gpu.py dataset/small-imagenet-1/ -b 1 --exp_name images1-bsize1-normalize
python main-nvidia-dali-gpu.py dataset/small-imagenet-16/ -b 1 --exp_name images16-bsize1-normalize
python main-nvidia-dali-gpu.py dataset/small-imagenet-16/ -b 16 --exp_name images16-bsize16-normalize