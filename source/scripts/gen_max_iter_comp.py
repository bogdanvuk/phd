import os
import numpy as np
import matplotlib.pyplot as plt
from table_fig_dual_feature import table_fig_dual_feature

max_iters = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000]
files = [os.path.join('results', 'EFTI_{}k.js'.format(f)) for f in max_iters]
titles = ['{}k'.format(f) for f in max_iters]
xvals = [i*1000 for i in max_iters]

table_fig_dual_feature(files, ['size', 'acc'], "max-iter-comp",
                       '../efti.rst', xvals=xvals,
                       cluster_by='acc', plot_funcs=(plt.semilogx, plt.semilogx),
                       subfig_caption = "DT {feature}: {datasets}",
                       titles=titles, locs=["lower right", "lower right"]
)
