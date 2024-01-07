import sys
import os

if len(sys.argv) <= 1:
    print("please provide gpu type. Exmaple: \"python parse-profiles.py p100\"")
    exit(0)

gpu_type = sys.argv[1]

models=['resnet50']

num_profile_batches = 50
batch_sizes = range(1,129)


for model in models:
    with open("{}/{}-avg.txt".format(gpu_type, model), "w") as f:
        f.write('batch_size\tgpu_time\n')
        for batch_size in batch_sizes:
            cpu2gpu_times = []
            gpu_times = []
            file_path = "{}/{}-batch{}.csv".format(gpu_type, model, batch_size)
            if os.path.exists(file_path):
                with open(file_path, 'r') as fread:
                    lines = fread.readlines()
                    for i in range(1, num_profile_batches+2):
                        line = lines[i]
                        numbers = line.strip().split('\t')
                        cpu2gpu_times.append(float(numbers[0]))
                        gpu_times.append(float(numbers[1]))
            else:
                print("{} does not exist!".format(file_path))
                exit(0)
            gpu_times.sort()
            gpu_times = gpu_times[0:-6]
            avg_gpu_time = sum(gpu_times)/len(gpu_times)
            medium_gpu_time = gpu_times[30]
            f.write('{}\t{}\n'.format(batch_size, avg_gpu_time))




