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

for i, res in enumerate([hw_res, arm_res, pc_res]):
    for d, r in res['res'].items():

        t = []

        for _,cv_run in r.items():
            for _,run in cv_run.items():
                t += [run['timing']]

        table[d][i] = sum(t)/len(t)



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
bar_width = 0.2
index = np.arange(len(datasets))

fig, ax = plt.subplots(figsize=(16,6), tight_layout=True)

rect_hw = plt.bar(index - 1.5*bar_width, exec_hw, bar_width,
                 alpha=opacity,
                 color='b',
                 label='HW/SW')

rect_hw = plt.bar(index-0.5*bar_width, exec_arm, bar_width,
                 alpha=opacity,
                 color='r',
                 label='HW/SW')

rect_hw = plt.bar(index+0.5*bar_width, exec_pc, bar_width,
                 alpha=opacity,
                 color='g',
                 label='HW/SW')


ax.yaxis.set_major_locator(MultipleLocator(250))
plt.xticks(range(len(datasets)), datasets)
plt.margins(0.03)
plt.tick_params(axis='both', which='major', labelsize=18)
savefig("test.png")
plt.show()
