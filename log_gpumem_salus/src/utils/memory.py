# from apex import amp
from torch.utils.checkpoint import checkpoint_sequential
import torch
import json
import time
from filelock import Timeout, FileLock
import psutil


def _get_gpu_mem(synchronize=True, empty_cache=True):
    return torch.cuda.memory_allocated(), torch.cuda.memory_cached()


def _generate_mem_hook(handle_ref, mem, idx, hook_type, exp):
    def hook(self, *args):
        if len(mem) == 0 or mem[-1]["exp"] != exp:
            call_idx = 0
        else:
            call_idx = mem[-1]["call_idx"] + 1

        mem_all, mem_cached = _get_gpu_mem()
        torch.cuda.synchronize()
        mem.append({
            'layer_idx': idx,
            'call_idx': call_idx,
            'layer_type': type(self).__name__,
            'exp': exp,
            'hook_type': hook_type,
            'mem_all': mem_all,
            'mem_cached': mem_cached,
        })

    return hook


def _add_memory_hooks(idx, mod, mem_log, exp, hr):
    h = mod.register_forward_pre_hook(_generate_mem_hook(hr, mem_log, idx, 'pre', exp))
    hr.append(h)

    h = mod.register_forward_hook(_generate_mem_hook(hr, mem_log, idx, 'fwd', exp))
    hr.append(h)

    h = mod.register_backward_hook(_generate_mem_hook(hr, mem_log, idx, 'bwd', exp))
    hr.append(h)


# def log_mem(model, inp, mem_log=None, exp=None):
#     mem_log = mem_log or []
#     exp = exp or f'exp_{len(mem_log)}'
#     hr = []
#     for idx, module in enumerate(model.modules()):
#         _add_memory_hooks(idx, module, mem_log, exp, hr)

#     try:
#         for i in range(2):
#             out = model(inp)
#             loss = out.sum()
#             loss.backward()
#     finally:
#         [h.remove() for h in hr]

#         return mem_log

def log_mem(num_script, model, inp, mem_log=None, exp=None):
    mem_log = mem_log or []
    exp = exp or f'exp_{len(mem_log)}'
    hr = []
    # for idx, module in enumerate(model.modules()):
    #     _add_memory_hooks(idx, module, mem_log, exp, hr)

    
    num_batches = 256
    # print("egpu ->", egpu)
    # quit()
    file_path = '/home/cc/edev/egpu0.json'
    lock_path = '/home/cc/edev/egpu0.json.lock'

    lock = FileLock(lock_path, timeout=1)
    current_second = 0
    fps_log = []
    time_log = []

    

    # Get memory usage
    memory_info = psutil.virtual_memory()

    # print(f"Total Memory: {memory_info.total} bytes")
    # print(f"Used Memory: {memory_info.used} bytes")
    # print(f"Free Memory: {memory_info.free} bytes")

    # quit()

    start_time_log = time.time()

    for i in range(num_batches):
        start_time = time.time()
        print("batch -->", i)
        
        with open('/home/cc/edev/egpu0.json', 'r') as file:
            json_data = file.read()
        print(json_data)
        egpu = json.loads(json_data)
        

        time.sleep(0.0140)
        
        # memmory for alexnet
        mem_max = 2552515072
        mem_min = 797564928

        # try multiple model
        
        # print(egpu["curr_mem"])
        # print(egpu["m_limit"])
        # print(egpu["curr_mem"] + mem_max)
        # print(egpu["curr_mem"] + mem_min)
        # print(egpu["m_limit"] > egpu["curr_mem"] + mem_max)
        # print(egpu["m_limit"] > egpu["curr_mem"] + mem_min)
        # quit()
        
        # add emulate time.sleep


        print(egpu["occupied"] )
        while (egpu["occupied"] == True) and (egpu["m_limit"] > egpu["curr_mem"] + mem_min):
            print("waiting..")
            time.sleep(0.001)
            with open('/home/cc/edev/egpu0.json', 'r') as file:
                # print("open..", file.read())
                json_data = file.read()
                print(json_data)
            egpu = json.loads(json_data)
            print("egpu ->", egpu)
            if egpu["occupied"] == False:
                egpu["curr_mem"] = mem_min
                egpu["curr_mem"] += mem_max

        print("no occupied in memory..")
        curr_gpu = inp.device.type
        # egpu = {
        #     "type": torch.cuda.get_device_name(0),
        #     "m_limit": torch.cuda.get_device_properties(0).total_memory,
        #     "occupied": True,
        #     "curr_mem": torch.cuda.memory_allocated(0)
        # }

        egpu["occupied"] == True

        # import threading
        # import time

        # def run():
        #     while True:
        #         print("background")
        #         time.sleep(.5)

        # thread = threading.Thread(target=run,daemon=True)
        # thread.start()
        
        # print(curr_gpu, egpu)
        # Convert to JSON
        with lock:
            with open("/home/cc/edev/egpu0.json", "w") as outfile: 
                json.dump(egpu, outfile)

        # out = model(inp)
        # loss = out.sum()
        # loss.backward()
        time.sleep(0.2032)
        
        # egpu = {
        #     "type": torch.cuda.get_device_name(curr_gpu),
        #     "m_limit": torch.cuda.get_device_properties(curr_gpu).total_memory,
        #     "occupied": False,
        #     "curr_mem": torch.cuda.memory_allocated(curr_gpu)
        # }

        egpu["occupied"] == True
        with lock:
            with open("/home/cc/edev/egpu0.json", "w") as outfile: 
                json.dump(egpu, outfile)
        # print("egpu ->", egpu)

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


def log_mem_cp(model, inp, mem_log=None, exp=None, cp_chunks=3):
    mem_log = mem_log or []
    exp = exp or f'exp_{len(mem_log)}'
    hr = []
    for idx, module in enumerate(model.modules()):
        _add_memory_hooks(idx, module, mem_log, exp, hr)

    try:
        out = checkpoint_sequential(model, cp_chunks, inp)
        loss = out.sum()
        loss.backward()
    finally:
        [h.remove() for h in hr]

        return mem_log


def log_mem_amp(model, inp, mem_log=None, exp=None):
    mem_log = mem_log or []
    exp = exp or f'exp_{len(mem_log)}'
    hr = []
    optimizer = torch.optim.SGD(model.parameters(), lr=0.01, momentum=0.9)
    amp_model, optimizer = amp.initialize(model, optimizer)
    for idx, module in enumerate(amp_model.modules()):
        _add_memory_hooks(idx, module, mem_log, exp, hr)

    try:
        out = amp_model(inp)
        loss = out.sum()
        with amp.scale_loss(loss, optimizer) as scaled_loss:
            scaled_loss.backward()
    finally:
        [h.remove() for h in hr]

        return mem_log


def log_mem_amp_cp(model, inp, mem_log=None, exp=None, cp_chunks=3):
    mem_log = mem_log or []
    exp = exp or f'exp_{len(mem_log)}'
    hr = []
    optimizer = torch.optim.SGD(model.parameters(), lr=0.01, momentum=0.9)
    amp_model, optimizer = amp.initialize(model, optimizer)
    for idx, module in enumerate(amp_model.modules()):
        _add_memory_hooks(idx, module, mem_log, exp, hr)

    try:
        out = checkpoint_sequential(amp_model, cp_chunks, inp)
        loss = out.sum()
        with amp.scale_loss(loss, optimizer) as scaled_loss:
            scaled_loss.backward()
    finally:
        [h.remove() for h in hr]

        return mem_log
