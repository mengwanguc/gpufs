import sys

with open(sys.argv[1], 'r') as f:
    lines = f.readlines()

io_times = []
for line in lines:
    if "Test" in line:
        break
    if 'io_time:' in line:
        io_time = float(line.strip().split("\t")[0].split(":")[1])
        io_times.append(io_time)

print(sum(io_times))