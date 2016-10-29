from os import listdir, path
from os.path import isfile, join
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import matplotlib
import csv
import pylab
import os
import json
import numpy as np

def to_percent(y, position):
    # Ignore the passed in position. This has the effect of scaling the default
    # tick locations.

    # The percent symbol needs escaping in latex
    if matplotlib.rcParams['text.usetex'] == True:
        return r"{}$\%$".format(int(y*100))
    else:
        return r"{}%".format(int(y*100))

gprof_res_file = '/data/projects/phd/source/scripts/profiling.js'
# gprof_res_file = '../scripts/profiling.js'

def load_js_data(fname):
    with open(fname) as data_file:
        res = json.load(data_file)

    return res

def profiling_plot(ds_slice, base_color, alpha_range=(0.3,1)):
    table = load_js_data(gprof_res_file)

    datasets = list(sorted(table.keys()))[ds_slice]
    percents = [1 - table[ds]['others'] for ds in sorted(table)][ds_slice]

    formatter = FuncFormatter(to_percent)

    m = min(percents) - 1

    colors = []
    for i in range(len(percents)):
        percents[i] -= m

    alphas = np.linspace(alpha_range[0], alpha_range[1], len(percents))
    rgba_colors = np.zeros((len(percents),4))
    # for red the first column needs to be one
    for i in range(3):
        rgba_colors[:,i] = base_color[i]
    # the fourth column needs to be your alphas
    rgba_colors[:, 3] = alphas

    opacity = 0.4
    bar_width = 0.5

    left = [i - bar_width/2 for i in range(len(datasets))]

    fig = plt.figure(figsize=(16,3), tight_layout=True)
    plt.bar(left, percents, bottom=[m]*len(datasets), width=0.5, color=rgba_colors)
    #plt.stem(range(len(datasets)), percents,  markersize=100, bottom=96)
    plt.xticks(range(len(datasets)), datasets)
    plt.margins(0.03)
    plt.ylim(0.7, 1);
    plt.locator_params(axis='y', nbins=4)
    plt.gca().yaxis.set_major_formatter(formatter)
    plt.gca().yaxis.grid(True)
    plt.tick_params(axis='both', which='major', labelsize=18)

    return plt
