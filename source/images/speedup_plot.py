import json
import csv
import numpy as np
from pylab import *
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from matplotlib.pyplot import xticks

arm_js = '/data/projects/rst/examples/paper/source/data/crossvalidation/arm.js'
hw_js = '/data/projects/rst/examples/paper/source/data/crossvalidation/hw.js'
pc_js = '/data/projects/rst/examples/paper/source/data/crossvalidation/pc.js'

with open(arm_js) as f:
    arm_res = json.load(f)
with open(hw_js) as f:
    hw_res = json.load(f)
with open(pc_js) as f:
    pc_res = json.load(f)

table = {}

for d in hw_res['dataset']:
    table[d] = [(), (), ()]

# for i, (res, run_name) in enumerate(zip([arm_res, pc_res], ["arm_run", "pc_run"])):
#     for r in res[run_name]:
#         d = r['dataset']
#         t = []
# 
#         t += [run['timing']]
# 
#     table[d][i+1] = sum(t)/len(t)

hw_run = []
if 'hw_run' in hw_res:
    hw_run.extend(hw_res['hw_run'])

hw_times = {}
for run in hw_run:
    dataset_name = run['dataset']
    if dataset_name not in hw_times:
        hw_times[dataset_name] = []
    
    hw_times[dataset_name].append(run['timing'])

for d, t in hw_times.items():
    table[d][0] = sum(t)/len(t)
    
pc_run = []
arm_run = []

for s, res, run in zip(['pc_run', 'arm_run'], [pc_res, arm_res], [pc_run, arm_run]):
    if s in res:
        run.extend(res[s])

pc_times = {}
arm_times = {}
for i,(timings, run_list) in enumerate(zip([arm_times, pc_times],[arm_run, pc_run])):
    for run in run_list:
        dataset_name = run['dataset']
        if dataset_name not in timings:
            timings[dataset_name] = []
            
        timings[dataset_name].append(run['timing'])

    for d, t in timings.items():
        table[d][i+1] = sum(t)/len(t)

spdup_arm = []
spdup_pc = []
datasets = []

exec_arm = []
exec_pc = []
exec_hw = []

for d,res in iter(sorted(table.items())):
    spdup_arm += [res[1]/res[0]]
    spdup_pc += [res[2]/res[0]]
    datasets += [d]
    exec_hw += [res[0]]
    exec_arm += [res[1]]
    exec_pc += [res[2]]

fs = 20
opacity = 0.4
bar_width = 0.5
index = np.arange(len(datasets))

fig, (ax0, ax1) = plt.subplots(figsize=(16,6), nrows=2, sharex=True, tight_layout=True)

ax0.bar(index - 0.5*bar_width, spdup_arm, bar_width,
                 alpha=opacity,
                 color='b',
                 label='HW/SW')
ax0.yaxis.set_major_locator(MultipleLocator(20))
ax0.yaxis.grid(True)
ax0.set_title('a) HW/SW speedup over the SW-ARM implementation', fontsize=fs, loc='left')
ax0.tick_params(axis='y', labelsize=18)

ax1.yaxis.set_major_locator(MultipleLocator(2))
ax1.bar(index - 0.5*bar_width, spdup_pc, bar_width,
                 alpha=opacity,
                 color='r',
                 label='HW/SW')
ax1.yaxis.grid(True)
ax1.set_title('b) HW/SW speedup over the SW-PC implementation', fontsize=fs, loc='left')
ax1.tick_params(axis='y', labelsize=18)

plt.xticks(range(len(datasets)), datasets)
plt.margins(0.03)
plt.tick_params(axis='x', which='major', labelsize=18)
# plot.tick_params(axis='both', which='minor', labelsize=18)

plt.show()
