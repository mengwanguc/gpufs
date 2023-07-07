create a 50GB dataset
```
cp -r ~/data/test-utilization ~/data/test-utilization-50g
python3 copy.py ~/data/test-utilization-50g/imagenette2/train/
```


find the number of files in that folder:
```
find ~/data/test-utilization-50g/imagenette2/train/ -type f | wc -l
```

I got 466233

In read.c and get_lsa.c, modify "#define NUM_FILES" value to 466233.
(It's now hardcoded. Sorry!)

```
make
python load.py ~/data/test-utilization-50g/imagenette2/train/ imagenet_train_file_paths
python sample.py 466233 10000 samples/samples_10000.txt
./get_lsa imagenet_train_file_paths
```

This generate 10000 random samples from all the files and get their inode and LBA information.

now samples info is in samples/samples_inodes_lba_10000.txt


mode 0: no sort
```
sudo bash clear-cache.sh
./read imagenet_train_file_paths 32 0 1 10000
```

mode 4: sort by LBA:
```
sudo bash clear-cache.sh
./read imagenet_train_file_paths 32 4 1 10000
```