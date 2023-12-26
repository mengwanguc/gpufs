import psutil
import GPUtil

def get_cpu_memory():
    mem = psutil.virtual_memory()
    return mem.total, mem.available, mem.percent

def get_gpu_memory():
    gpu_list = GPUtil.getGPUs()
    gpu_info = []
    
    for gpu in gpu_list:
        gpu_info.append({
            'id': gpu.id,
            'name': gpu.name,
            'total': gpu.memoryTotal,
            'free': gpu.memoryFree,
            'used': gpu.memoryUsed,
            'percent': gpu.memoryUtil * 100
        })
    
    return gpu_info

# Get CPU memory information
total_cpu, available_cpu, percent_cpu = get_cpu_memory()
print(f"Total CPU Memory: {total_cpu} bytes")
print(f"Available CPU Memory: {available_cpu} bytes")
print(f"CPU Memory Usage: {percent_cpu}%")

# Get GPU memory information
gpu_info = get_gpu_memory()
for gpu in gpu_info:
    print(f"\nGPU {gpu['id']} ({gpu['name']}):")
    print(f"Total GPU Memory: {gpu['total']} bytes")
    print(f"Free GPU Memory: {gpu['free']} bytes")
    print(f"Used GPU Memory: {gpu['used']} bytes")
    print(f"GPU Memory Usage: {gpu['percent']}%")


import torch

def get_gpu_memory():
    gpu_info = []

    # Check if CUDA is available
    if torch.cuda.is_available():
        for i in range(torch.cuda.device_count()):
            gpu = torch.cuda.get_device_properties(i)
            gpu_info.append({
                'id': i,
                'name': gpu.name,
                'total': torch.cuda.get_device_properties(i).total_memory,
                'free': torch.cuda.get_device_properties(i).free_memory,
                'used': torch.cuda.get_device_properties(i).total_memory - torch.cuda.get_device_properties(i).free_memory,
                'percent': (1 - torch.cuda.get_device_properties(i).free_memory / torch.cuda.get_device_properties(i).total_memory) * 100
            })
    else:
        print("CUDA is not available.")

    return gpu_info

# Get GPU memory information
gpu_info = get_gpu_memory()

# Print GPU memory information
for gpu in gpu_info:
    print(f"\nGPU {gpu['id']} ({gpu['name']}):")
    print(f"Total GPU Memory: {gpu['total']} bytes")
    print(f"Free GPU Memory: {gpu['free']} bytes")
    print(f"Used GPU Memory: {gpu['used']} bytes")
    print(f"GPU Memory Usage: {gpu['percent']:.2f}%")

