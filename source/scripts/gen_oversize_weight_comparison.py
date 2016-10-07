import sys
import os
import numpy as np
from sklearn.cluster import KMeans
sys.path.append(os.path.expandvars('$EFTI/script'))
from rank import load_data, form_mean_table, dump_table_csv
import matplotlib.pyplot as plt
from table_fig_dual_feature import table_fig_dual_feature

oversize_weights = [0, 0.001, 0.01, 0.02, 0.06, 0.1, 0.2]
files = [os.path.join('results',
                      'EFTI_500k.js' if ow == 0.02 else 'EFTI_500k_ow-{}.js'.format(ow))
         for ow in oversize_weights]

titles = ['{}'.format(ow) for ow in oversize_weights]
xvals = [0.0001] + oversize_weights[1:]

caption = "The figure shows the dependencies of the DT sizes and accuracies on the oversize weight (|Ko|) parameter values. DT sizes and accuracies are displayed for five datasets per subfigure."

table_fig_dual_feature(files, ['size', 'acc'], "oversize-comp",
                       '../efti.rst', xvals=xvals,
                       cluster_by='acc', plot_funcs=(plt.loglog, plt.semilogx),
                       subfig_caption = "DT {feature}: {datasets}",
                       fig_caption = caption,
                       titles=titles, locs=["upper right", "upper right"]
)
