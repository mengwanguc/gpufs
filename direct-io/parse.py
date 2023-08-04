import sys
import matplotlib.pyplot as plt

sizes = []
average_latencies = []

with open(sys.argv[1], 'r') as f:
    lines = f.readlines()
    for line in lines:
        data = line.strip().split('\t')
        size = int(data[0].split('KB')[0])
        latencies = data[1:]
        total = 0
        for latency in latencies:
            total += int(latency)
        average_latency = total / len(latencies)
        sizes.append(size)
        average_latencies.append(average_latency)
    
print(len(sizes))

plt.plot(sizes[30000:30200],average_latencies[30000:30200], 'r')
plt.savefig('latency_by_distance.png')