To use the emulator, first update and rebuild pytorch-meng and torchvision-meng:

```
cd ~/pytorch-meng
git checkout emulator
python setup.py install
```

and

```
cd ~/torchvision-meng
git checkout emulator
python setup.py install
```

Then go back to this folder: `~/gpufs/emulator/datastall`.

Example for running emulator code:

```
python main-measure-time-emulator.py --gpu-type=p100 --gpu-count=1 --arch=alexnet --emulator-version=1 -j 4 ~/data/test-accuracy/imagenette2
```