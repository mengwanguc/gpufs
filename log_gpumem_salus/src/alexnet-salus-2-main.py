import time
time.sleep(15)

# %% Imports
import pandas as pd
import torch
from torch import nn
from torchvision.models import resnet18, mobilenet_v2, alexnet

# from src.utils.memory import log_mem, log_mem_amp, log_mem_amp_cp, log_mem_cp
# from src.utils.plot import plot_mem, pp
import time

# from apex import amp
from torch.utils.checkpoint import checkpoint_sequential
import torch
import json
import time
from filelock import Timeout, FileLock
# import psutil

import json
import threading
import time

def read_json(filename, lock):
    with lock:
        # Read the JSON content
        with open(filename, 'r') as file:
            data = json.load(file)

        if file == "":
            with open(filename, 'r') as file:
                data = json.load(file)

        return data

def modify_json(filename, lock, egpu):
    with lock:
        # Write back the modified JSON data
        with open(filename, 'w') as file:
            json.dump(egpu, file, indent=2)


def log_mem(num_script, file_path, model, inp, mem_log=None, exp=None):
    mem_log = mem_log or []
    exp = exp or f'exp_{len(mem_log)}'
    hr = []
    # for idx, module in enumerate(model.modules()):
    #     _add_memory_hooks(idx, module, mem_log, exp, hr)

    
    num_batches = 100
    # print("egpu ->", egpu)
    # quit()
    current_second = 0
    fps_log = []
    time_log = []

    # Create a lock
    json_file_lock = threading.Lock()
    print("json_file_lock ->", json_file_lock)

    try: 
        egpu = read_json(file_path, json_file_lock)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    print(egpu)

    start_time_log = time.time()

    for i in range(num_batches):
        start_time = time.time()
        print("batch -->", i)      

        time.sleep(0.0140)
        
        # memmory for alexnet
        mem_max = 2447713280
        mem_min = 553078784

        try: 
            egpu = read_json(file_path, json_file_lock)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        print("egpu1 ->", egpu)

        if (egpu["occupied"] == True):
            print("waiting..")
        while (egpu["occupied"] == True) :
            # and (egpu["m_limit"] > egpu["curr_mem"] + mem_min)
            time.sleep(0.001)
            try: 
                egpu = read_json(file_path, json_file_lock)
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
            # if json_data == "":
            #     continue
            # egpu = json.loads(json_data)
            # print("egpu ->", egpu)
            if egpu["occupied"] == False:
                # egpu["occupied"] = True
                # modify_json(file_path, json_file_lock, egpu)
                egpu["curr_mem"] = mem_min
                egpu["curr_mem"] += mem_max
                

        egpu["occupied"] = True
        print("egpu true->",egpu)
        
        modify_json(file_path, json_file_lock, egpu)

        # out = model(inp)
        # loss = out.sum()
        # loss.backward()
        print("training..")
        # time.sleep(10)
        time.sleep(0.5)

        egpu["occupied"] = False
        print("egpu1 ->", egpu)
        modify_json(file_path, json_file_lock, egpu)

        end_time = time.time()

        # Calculate FPS
        time_per_iteration = end_time - start_time
        fps = 256 / time_per_iteration
        print(time_per_iteration)
        print(fps)

        # Log FPS and time every second
        if int(end_time) > current_second:
            fps_log.append(round(fps, 0))
            if num_script == 1:
                time_log.append(end_time - start_time_log)
            elif num_script == 2:
                time_log.append(end_time - start_time_log + 15)
            elif num_script == 3:
                time_log.append(end_time - start_time_log + 30)
            current_second += 1

    # Save the logs to text files
    with open("/home/cc/gpufs/log_gpumem_salus/src/fps_log"+str(num_script)+".txt", "w") as fps_file:
        for fps in fps_log:
            fps_file.write(f"{fps:.2f}\n")

    with open("/home/cc/gpufs/log_gpumem_salus/src/time_log"+str(num_script)+".txt", "w") as time_file:
        for timestamp in time_log:
            time_file.write(f"{timestamp}\n")
    
    [h.remove() for h in hr]
    print("test ->", hr)
    return mem_log


base_dir = '.'
# %% Analysis baseline

model = alexnet().cpu()
bs = 512
input = torch.rand(bs, 3, 512, 512).cpu()
# print()

mem_log = []


file_path = "/home/cc/gpufs/log_gpumem_salus/src/edev/egpu0.json"
start = time.time()
mem_log.extend(log_mem(2, file_path, model, input, exp=f'batch size {bs}'))
print("mem_log ->", mem_log)

end = time.time() - start
print("training time ->",end)

# pp(df, exp='baseline')

# torch.cuda.synchronize()
# torch.cuda.empty_cache()

# bs = 512
# input = torch.rand(bs, 3, 224, 224).cuda()

# try:
#     mem_log.extend(log_mem(model, input, exp=f'batch size {bs}'))
# except Exception as e:
#     print(f'log_mem failed because of {e}')

# torch.cuda.synchronize()
# torch.cuda.empty_cache()

# bs = 256
# input = torch.rand(bs, 3, 224, 224).cuda()

# try:
#     mem_log.extend(log_mem(model, input, exp=f'batch size {bs}'))
# except Exception as e:
#     print(f'log_mem failed because of {e}')

# torch.cuda.synchronize()
# torch.cuda.empty_cache()

# bs = 128
# input = torch.rand(bs, 3, 224, 224).cuda()

# try:
#     mem_log.extend(log_mem(model, input, exp=f'batch size {bs}'))
# except Exception as e:
#     print(f'log_mem failed because of {e}')

# torch.cuda.synchronize()
# torch.cuda.empty_cache()

# bs = 64
# input = torch.rand(bs, 3, 224, 224).cuda()

# try:
#     mem_log.extend(log_mem(model, input, exp=f'batch size {bs}'))
# except Exception as e:
#     print(f'log_mem failed because of {e}')


df = pd.DataFrame(mem_log)
df.to_csv('out.csv', index=False)
print(df)


# plot_mem(df, output_file=f'{base_dir}/alexnet_memory_plot_all.png',
#          title = 'GPU Memory Usage of Alexnet in one batch over time')


'''
# %% Create Sequential version of model
class Flatten(nn.Module):
    def forward(self, x):
        return torch.flatten(x, 1)


seq_model = nn.Sequential(
    model.conv1,
    model.bn1,
    model.relu,
    model.maxpool,
    model.layer1,
    model.layer2,
    model.layer3,
    model.layer4,
    model.avgpool,
    Flatten(),
    model.fc,
)

# %% Test models are identical:

with torch.no_grad():
    out = model(input)
    seq_out = seq_model(input)
    max_diff = (out - seq_out).max().abs().item()
    assert max_diff < 10 ** -10

# %%  Log mem optims

try:
    mem_log.extend(log_mem_cp(seq_model, input, cp_chunks=3, exp='3_checkpoints'))
except Exception as e:
    print(f'log_mem_cp failed because of {e}')

torch.cuda.synchronize()
torch.cuda.empty_cache()

try:
    mem_log.extend(log_mem_amp(model, input, exp='auto_mixed_precision'))
except Exception as e:
    print(f'log_mem_amp failed because of {e}')

torch.cuda.synchronize()
torch.cuda.empty_cache()

try:
    mem_log.extend(log_mem_amp_cp(seq_model, input, cp_chunks=3, exp='amp_and_3_cp'))
except Exception as e:
    print(f'log_mem_amp_cp failed because of {e}')

torch.cuda.synchronize()
torch.cuda.empty_cache()

# %% Plot all files

df = pd.DataFrame(mem_log)

plot_mem(df, output_file=f'{base_dir}/resnet50_all_memory_plot_{bs}.png')

# %% Get max memory

(
    df.groupby('exp').mem_all.max().sort_values(ascending=False)
        .plot('bar').get_figure().savefig(f'{base_dir}/resnet50_max_mem_hist_{bs}.png')
)
'''
