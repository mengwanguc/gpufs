import sys
import os

if len(sys.argv) <= 1:
    print("please provide gpu type. Exmaple: \"python parse-profiles.py p100\"")
    exit(0)

gpu_type = sys.argv[1]

models=['alexnet']

num_profile_batches = 50
batch_sizes = range()

with open("{}/avg.txt".format(gpu_type), "w") as f:
    for model in models:
        f.write("model: {}\n".format(model))
        cpu2gpu_times_per_batchsize = []
        gpu_times_per_batchsize = []
        cpu2gpu_times = []
        gpu_times = []
        file_path = "{}/{}-batch{}.csv".format(gpu_type, model, batch_size)
        if os.path.exists(file_path):
            with open(file_path, 'r') as fread:
                lines = fread.readlines()
                for i in range(1, num_profile_batches+2):
                    line = lines[i]
                    if i > 5:
                        numbers = line.strip().split('\t')
                        cpu2gpu_times.append(numbers[0])
                        gpu_times.append(numbers[1])
        else:
            print("{} does not exist!".format(file_path))
            exit(0)
        f.write('gpu_time\n')
        for gpu_time in gpu_times:




