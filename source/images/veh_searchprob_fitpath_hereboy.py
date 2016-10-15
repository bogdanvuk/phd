from plot_searchprob_fitpath import plot_fitpath_comp, to_k
from matplotlib.patches import Ellipse
import matplotlib
import os

fns = ['../data/searchprob/veh_fitpath_vanilla.js', '../data/searchprob/veh_fitpath_hereboy.js']
plt = plot_fitpath_comp(fns, labels=['Greedy', 'Hereboy'], aspect=0.8)


plt.gca().set_xlim([0,15000])
plt.gca().set_ylim([0.49,0.71])
plt.gca().xaxis.set_major_formatter(to_k)
plt.xlabel('iteration', fontsize=16)
plt.ylabel('fitness', fontsize=16)
# plt.gca().add_patch(plt.Circle((2000, 0.58), 200, color='b', fill=False))
# plt.gca().add_patch(Ellipse((2100, 0.58), 2000, 0.035, color='r', fill=False, linewidth=5))
annot_opts = dict(xycoords='data',
                 textcoords='data',
                 arrowprops=dict(facecolor='red', shrink=0.05, width=4),
                 horizontalalignment='right', verticalalignment='top',
                 fontsize = 20)

plt.gca().annotate('1', xy=(2300, 0.604),
                   xytext=(1000, 0.64), **annot_opts)

plt.gca().annotate('1', xy=(4100, 0.624),
                   xytext=(5300, 0.666), **annot_opts)

plt.gca().annotate('1', xy=(9516, 0.641),
                   xytext=(9400, 0.690), **annot_opts)

plt.gca().annotate('2', xy=(11480, 0.653),
                   xytext=(13500, 0.684), **annot_opts)

plt.gca().annotate('3', xy=(5260, 0.536),
                   xytext=(2000, 0.517), **annot_opts)

plt.gca().annotate('3', xy=(11900, 0.556),
                   xytext=(7800, 0.577), **annot_opts)

plt.locator_params(axis='both', nbins=6);
plt.tick_params(axis='both', which='major', labelsize=16)
plt.gca().text(1000, 0.68,'veh', fontsize=30)
plt.show()
