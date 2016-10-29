import sys
# from table_fig_dual_feature import make_feature_comp_tables
import os
sys.path.append(os.path.expandvars('$EFTI/script'))
from rank import form_mean_table, load_js_data, write_csv_table, mean_confidence_interval
from collections import OrderedDict

files = [
    'cv_arm.js',
    'EFTI_500k_timing_delta.js',
]
title_fmt_dbl = r':raw:`\multicolumn{{1}}{{>{{\centering\arraybackslash}}m{{20mm}}}}{{{}}}`'
title_fmt_single = r":raw:`\multicolumn{{1}}{{c}}{{{}}}`"
title_fmts = [title_fmt_single, title_fmt_single, title_fmt_dbl, title_fmt_single, title_fmt_dbl]

files = [os.path.join('results', f) for f in files]
titles = ['HW/SW [s]', r'SW-ARM', r'Speedup SW-ARM', r'SW-PC', r'Speedup SW-PC']
row_features = [ 'cv_hw_run', 'cv_arm_run', 'speedup_cv_arm_run', 'cv_pc_run', 'speedup_cv_pc_run']
features = ['cv_pc_run', 'cv_arm_run', 'cv_hw_run']
comp = ['cv_pc_run', 'cv_arm_run']

def load_data(files):
    data = {}
    for fh in files:
        res = load_js_data(fh)

        for f in features:
            if f in res:
                for r in res[f]:
                    ds = r['dataset']

                    if ds not in data:
                        data[ds] = {}

                    if f not in data[ds]:
                        data[ds][f] = []

                    data[ds][f].append(r['time'])

    return data

def calc_speedup(table, base, comp):
    speedup = {}
    for c in comp:
        speedup[c] = {}
        for ds in table:
            speedup[c][ds] = table[ds][c][0] / table[ds][base][0]

    return speedup

data = load_data(files)
table = form_mean_table(data)

speedup = calc_speedup(table, 'cv_hw_run', comp)
avg_speedup = {c:0 for c in comp}
for ds in table:
    for c in comp:
        table[ds]['speedup_{}'.format(c)] = speedup[c][ds]
        avg_speedup[c] += speedup[c][ds]

for c in comp:
    avg_speedup[c] = mean_confidence_interval(list(speedup[c].values()), confidence=0.95)

head_row = [title_fmt_single.format('Dataset')] + [f.format(t) for f,t in zip(title_fmts,titles)]
csv_table = [head_row]

for d,res in iter(sorted(table.items())):
    row = [d]

    for a in row_features:
        if a in res:
            if a.startswith('speedup'):
                row.append(r':math:`{:.2f}`'.format(res[a]))
            else:
                row.append(r':math:`{0:0.2f} \pm {1:05.2f}`'.format(res[a][0], res[a][1]))
        else:
            row += ["-"]

    csv_table.append(row)

csv_table.append([r":raw:`\bottomrule Avg.`", ''] +
                 ['', r':math:`{0:0.2f} \pm {1:04.2f}`'.format(*avg_speedup['cv_arm_run'])] +
                 ['', r':math:`{0:0.2f} \pm {1:04.2f}`'.format(*avg_speedup['cv_pc_run'])]
                 )

write_csv_table("cop-speedup.csv", csv_table, horizontal_splits=1)
pass

# make_feature_comp_tables(files, ['time'], 'delta-comp', horizontal_splits=2, titles=titles,
#                          head_fmt=r':raw:`\multicolumn{{1}}{{>{{\centering\arraybackslash}}p{{23mm}}}}{{{}}}`',
#                          data_fmt=r':math:`{0:0.2f} \pm {1:05.2f}`')
