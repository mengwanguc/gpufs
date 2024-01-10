# %% Imports
import pandas as pd
import torch
from torch import nn
from torchvision.models import resnet50, mobilenet_v2, alexnet, resnet18

from utils.memory import log_mem, log_mem_amp, log_mem_amp_cp, log_mem_cp
from utils.plot import plot_mem_by_time, pp

import pycuda.driver as cuda
from pycuda.tools import DeviceMemoryPool, OccupancyRecord
from pycuda.compiler import SourceModule
import torchvision.transforms as transforms
import time

import torch.backends.cudnn as cudnn

cudnn.benchmark = True




# # Initialize the CUDA device
# cuda.init()

# # Select the first CUDA device
# device = cuda.Device(0)

# # Create a CUDA context on the device
# context = device.make_context()

def print_memory_pycuda():
    free_memory, total_memory = cuda.mem_get_info()
    used_memory = total_memory - free_memory
    print(f"Total: {total_memory / 1024**2} MB\t"
          f"Free: {free_memory / 1024**2} MB\t" 
          f"Used: {used_memory / 1024**2} MB")


base_dir = '.'
# %% Analysis baseline

model = resnet18().cuda()
bs = 256
input = torch.rand(bs, 3, 224, 224)
input = input.cuda(0)

target = torch.ones(bs)
target = target.type(torch.LongTensor)
target = target.cuda(0)

mem_log = []


l = log_mem(model, input, target, exp=f'batch size {bs}')
mem_log.extend(l)


torch.cuda.synchronize()

print_memory_pycuda()

torch.cuda.empty_cache()

df = pd.DataFrame(mem_log)

print(df)


print('pytorch total: {}  cached: {}'.format(torch.cuda.memory_allocated()/ 1024**2, torch.cuda.memory_reserved()/ 1024**2))


          
print_memory_pycuda()

plot_mem_by_time(df, output_file=f'{base_dir}/alexnet_memory_plot_all.png',
         title = 'GPU Memory Usage of Alexnet in one batch over time')



# Clean up and free all memory allocated by PyCUDA
context.pop()



