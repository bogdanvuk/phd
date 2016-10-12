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

max_iters = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000]
files = [os.path.join('results', 'EFTI_{}k.js'.format(f)) for f in max_iters]
titles = ['{}k'.format(f) for f in max_iters]
xvals = [i*1000 for i in max_iters]

fig_caption =[
    "Dependency of the induced DT sizes and accuracies on the number of iterations the |algo| algorithm was run. Datasets 1-25.",
    "Dependency of the induced DTs on the number of iterations the |algo| algorithm was run. Datasets 25-50."
    ]

table_fig_dual_feature(files, ['size', 'acc'], "max-iter-comp",
                       '../efti.rst', xvals=xvals,
                       figs=figs, aspect=0.5,
                       cluster_by=None, plot_funcs=(plt.semilogx, plt.semilogx),
                       subfig_caption = "DT {feature}: {datasets}",
                       fig_caption = fig_caption,
                       titles=titles, locs=["lower right", "lower right"]
)
