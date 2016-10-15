from plot_searchprob_fitpath import plot_fitpath_comp, to_k
from matplotlib.patches import Ellipse
import matplotlib
import os

fns = ['../data/searchprob/veh_fitpath_vanilla.js', '../data/searchprob/veh_fitpath_metropolis.js']
# fns = ['../data/searchprob/veh_fitpath_metropolis.js', '../data/searchprob/veh_fitpath_metropolis_rp.js']
plt = plot_fitpath_comp(fns, labels=['Greedy', 'Metropolis'], aspect=0.8)


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

# plt.gca().annotate('1', xy=(1800, 0.5845),
#                    xytext=(700, 0.60), **annot_opts)

# plt.gca().annotate('2', xy=(2300, 0.583),
#                    xytext=(3500, 0.608), **annot_opts)

# plt.gca().annotate('3', xy=(8800, 0.56),
#                    xytext=(10500, 0.58), **annot_opts)

plt.locator_params(axis='both', nbins=6);
plt.tick_params(axis='both', which='major', labelsize=16)
plt.gca().text(1000, 0.62,'veh', fontsize=30)
plt.show()
