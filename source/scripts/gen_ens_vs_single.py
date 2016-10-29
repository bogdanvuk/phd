import os
from table_fig_dual_feature import make_feature_comp_tables

files = [
    'EFTI_50k_ow-0.01.js',
    'EEFTI_50k_3m_ow-0.01.js',
    'EEFTI_50k_5m_ow-0.01.js',
    'EEFTI_50k_9m_ow-0.01.js',
    'EEFTI_50k_17m_ow-0.01.js',
    'EEFTI_50k_33m_ow-0.01.js',
]

files = [os.path.join('results', f) for f in files]
titles = [1, 3, 5, 9, 17, 33]
make_feature_comp_tables(files, ['acc'], 'ens-vs-single', horizontal_splits=1, titles=titles,
                         head_fmt=r":raw:`\multicolumn{{1}}{{c}}{{{}}}`",
                         data_fmt=r':math:`{0:0.2f} \pm {1:0.2f}`')

make_feature_comp_tables(files, ['acc'], 'ens-vs-single-rank', horizontal_splits=2, titles=titles,
                         head_fmt=r":raw:`\multicolumn{{1}}{{r}}{{{}}}`",
                         data_fmt=r'{}', rank=True,
                         rank_avg=[r":raw:`\\ \bottomrule \multicolumn{7}{c|}{\textbf{Rank}})`"])
