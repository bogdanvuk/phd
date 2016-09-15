from os import listdir, path
from os.path import isfile, join
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import matplotlib
import csv
import pylab
import os

def to_percent(y, position):
    # Ignore the passed in position. This has the effect of scaling the default
    # tick locations.
    s = str(y)

    # The percent symbol needs escaping in latex
    if matplotlib.rcParams['text.usetex'] == True:
        return s + r'$\%$'
    else:
        return s + '%'

#gmon_csv_path = '/home/bvukobratovic/projects/rst/examples/paper/source/data/profiling'
gmon_csv_path = '../../data/profiling'

files = sorted([ f for f in listdir(gmon_csv_path)
                if isfile(join(gmon_csv_path,f)) and path.splitext(f)[1] == '.csv' ], key=str.lower)


datasets = []
percents = []

for f in files:

    with open(join(gmon_csv_path,f), 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')

        fit_eval_perc = 0

        for row in spamreader:
            if row[0] in ['evaluate_node_test', 'find_dt_leaf_for_inst', 'find_node_distribution', 'fitness_eval']:
                fit_eval_perc += float(row[3])

        datasets.append(path.splitext(f)[0])
        percents.append(fit_eval_perc)

formatter = FuncFormatter(to_percent)

# print('AVG:', sum(percents)/len(percents))

m = min(percents) - 1

for i in range(len(percents)):
    percents[i] -= m

opacity = 0.4
bar_width = 0.5

left = [i - bar_width/2 for i in range(len(datasets))]

fig = plt.figure(figsize=(16,4), tight_layout=True)
plt.bar(left, percents, bottom=[m]*len(datasets), alpha=opacity, width=0.5)
#plt.stem(range(len(datasets)), percents,  markersize=100, bottom=96)
plt.xticks(range(len(datasets)), datasets)
plt.margins(0.03)
plt.gca().yaxis.set_major_formatter(formatter)
plt.gca().yaxis.grid(True)
plt.tick_params(axis='both', which='major', labelsize=18)
# fig.tight_layout()
plt.show()
