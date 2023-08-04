import random
import sys

if len(sys.argv) < 4:
    print('python sample.py <total_num> <sample_num> <output_file>')
    print('example: python sample.py 10000 100 samples_100000.txt')
    exit()



total = int(sys.argv[1])
sample_num = int(sys.argv[2])

samples = random.sample(range(total), sample_num)

with open(sys.argv[3], 'w') as f:
    for sample in samples:
        f.write('{}\n'.format(sample))