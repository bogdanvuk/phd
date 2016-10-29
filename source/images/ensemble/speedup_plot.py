import json
import csv
import numpy as np
from pylab import *
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from matplotlib.pyplot import xticks

spdup_arm = [[] for _ in range(5)]
spdup_pc = [[] for _ in range(5)]
datasets = []

with open('/data/projects/phd/source/scripts/co_ens_results.csv', 'r', newline='') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
    iterreader = iter(csvreader)
    # Skip headers
    next(iterreader)
    next(iterreader)
    for row in iterreader:
        for i in range(5):
            spdup_arm[i] += [float(row[i+1])]
            spdup_pc[i] += [float(row[i+6])]

        datasets += [row[0]]

# Remove the average line
datasets = datasets[:-1]
for i in range(5):
    spdup_arm[i] = spdup_arm[i][:-1]
    spdup_pc[i] = spdup_pc[i][:-1]

print(spdup_arm)
print(spdup_pc)
print(datasets)

fs = 18
opacity = 0.4
bar_width = 0.15
index = np.arange(len(datasets))

fig, (ax0, ax1) = plt.subplots(figsize=(16,6), nrows=2, sharex=True, tight_layout=True)

for i in range(5):
#     print(index - (i - 2.5)*bar_width)
    ax0.bar(index + (i - 2.5)*bar_width, spdup_arm[i], width=bar_width,
                     alpha=opacity,
                     color='b')
    
ax0.yaxis.set_major_locator(MultipleLocator(20))
ax0.yaxis.grid(True)
ax0.set_title('a) HW/SW speedup over SW-ARM implementation', fontsize=fs, loc='left')

for i in range(5):
    ax1.bar(index + (i - 2.5)*bar_width, spdup_pc[i], width=bar_width,
                     alpha=opacity,
                     color='r')
ax1.yaxis.grid(True)
ax1.set_title('b) HW/SW speedup over SW-PC implementation', fontsize=fs, loc='left')
plt.xticks(range(len(datasets)), datasets)
plt.margins(0.03)
plt.tick_params(axis='both', which='major', labelsize=18)

plt.show()
