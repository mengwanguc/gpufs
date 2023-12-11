import sys
import os

if len(sys.argv) <= 1:
    print("please provide gpu type. Exmaple: \"python parse-profiles.py p100\"")
    exit(0)

gpu_type = sys.argv[1]

models=['alexnet',
        'resnet18',
        'mobilenet_v2']

batch_sizes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 64, 128, 256]

num_profile_batches = 10

with open("{}/all.txt".format(gpu_type), "w") as f:
    for model in models:
        f.write("model: {}\n".format(model))
        cpu2gpu_times_per_batchsize = []
        gpu_times_per_batchsize = []
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
                        cpu2gpu_times.append(numbers[0])
                        gpu_times.append(numbers[1])
            else:
                for i in range(num_profile_batches+1):
                    cpu2gpu_times.append('N/A')
                    gpu_times.append('N/A')
            cpu2gpu_times_per_batchsize.append(cpu2gpu_times)
            gpu_times_per_batchsize.append(gpu_times)
        head = ""
        for batch_size in batch_sizes:
            head += "cpu2gpu_batch{}".format(batch_size)
            head += '\t'
            head += "gpu_batch{}".format(batch_size)
            head += '\t'
        f.write(head+'\n')
        for i in range(num_profile_batches+1):
            line = ""
            for j in range(len(batch_sizes)):
                line += str(cpu2gpu_times_per_batchsize[j][i])
                line += '\t'
                line += str(gpu_times_per_batchsize[j][i])
                line += '\t'
            f.write(line+'\n')
        f.write('\n')



