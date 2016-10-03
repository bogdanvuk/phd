import os
from table_fig_dual_feature import make_feature_comp_tables

files = [
    'EFTI_500k.js',
    'EFTI_500k_delta.js',
]

files = [os.path.join('results', f) for f in files]
titles = ['No delta', 'delta']
make_feature_comp_tables(files, ['time'], 'delta-comp', horizontal_splits=2, titles=titles)
