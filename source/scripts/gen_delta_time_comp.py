import os
from table_fig_dual_feature import make_feature_comp_tables

files = [
    'EFTI_500k.js',
    'EFTI_500k_timing_delta.js',
]

files = [os.path.join('results', f) for f in files]
titles = ['Original', r'Partial reclassification']
make_feature_comp_tables(files, ['time'], 'delta-comp', horizontal_splits=2, titles=titles,
                         head_fmt=r':raw:`\multicolumn{{1}}{{>{{\centering\arraybackslash}}p{{23mm}}}}{{{}}}`',
                         data_fmt=r':math:`{0:0.2f} \pm {1:05.2f}`')
