import sys

with open(sys.argv[1], 'r') as f:
    lines = f.readlines()

lats = []

for line in lines:
    lats.append(int(line.strip()))

lats.sort()

step = 1 / len(lats)

cdf = 0

with open(sys.argv[1]+'.cdf', 'w') as f:
    for lat in lats:
        cdf += step
        f.write('{} {}\n'.format(cdf, lat))
