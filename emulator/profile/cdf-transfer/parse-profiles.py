import sys
import os

if len(sys.argv) <= 1:
    print("please provide gpu type. Exmaple: \"python parse-profiles.py p100\"")
    exit(0)

gpu_type = sys.argv[1]

models=['alexnet']

num_profile_batches = 50
batch_sizes = range(1,177)


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
            cpu2gpu_times.sort()
            cpu2gpu_times = cpu2gpu_times[0:-6]
            avg_cpu2gpu_time = sum(cpu2gpu_times)/len(cpu2gpu_times)
            f.write('{}\t{}\n'.format(batch_size, avg_cpu2gpu_time))




