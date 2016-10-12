import os
import numpy as np
import matplotlib.pyplot as plt
from table_fig_dual_feature import table_fig_dual_feature

figs = [
    ['ger', 'sick', 'ca', 'vote', 'wilt'], # acc>0.9, size <=3
    ['bcw', 'irs', 'msh', 'psd', 'thy'], # acc>0.9, size <=5
    ['ausc', 'bank', 'ca', 'hep', 'hrts'], # acc>0.85, size <=5
    ['ion', 'sb', 'spect', 'thy', 'bc'], # acc>0.85, size <=5
    ['son', 'w21', 'adult', 'car', 'magic'], # acc>0.8, size <=7
    ['zoo', 'shuttle', 'seg', 'page', 'gls'], # acc>0.6, size <=30
    ['nurse', 'pen', 'pid', 'w40', 'ctg'], # acc>0.77, size <=30
    ['cvf', 'hrtc', 'jvow', 'liv', 'ttt'], # acc>0.7, size <=30
    ['spf', 'veh', 'vow', 'cmc', 'wine'], # acc>0.56, size <=40
    ['eb', 'eye', 'krkopt', 'letter', 'bch'], #
]

oversize_weights = [0, 0.001, 0.01, 0.02, 0.06, 0.1, 0.2]
files = [os.path.join('results',
                      'EFTI_500k.js' if ow == 0.02 else 'EFTI_500k_ow-{}.js'.format(ow))
         for ow in oversize_weights]

titles = ['{}'.format(ow) for ow in oversize_weights]
xvals = [0.0001] + oversize_weights[1:]

fig_caption =[
    "Dependencies of the induced DT sizes and accuracies on the oversize weight (|Ko|) parameter values. Datasets 1-25.",
    "Dependencies of the induced DT sizes and accuracies on the oversize weight (|Ko|) parameter values. Datasets 25-50."
    ]

table_fig_dual_feature(files, ['size', 'acc'], "oversize-comp",
                       '../efti.rst', xvals=xvals,
                       figs=figs, aspect=0.5,
                       cluster_by=None, plot_funcs=(plt.loglog, plt.semilogx),
                       subfig_caption = ["DT size: {datasets}",
                                         "DT accuracy: {datasets}"],
                       fig_caption = fig_caption,
                       titles=titles, locs=["upper right", "upper right"]
)
