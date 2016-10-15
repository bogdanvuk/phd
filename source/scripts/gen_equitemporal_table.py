#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.expandvars('$EFTI/script'))
from rank import load_js_data, mean_confidence_interval
from efti_intf import efti_test
from rank import load_data, form_mean_table, prepare_csv_table, write_csv_table
from table_fig_dual_feature import make_feature_comp_tables
import math

algo_js_tmplt = 'results/{}.js'
efti_compare_js_tmplt = 'results/equi_temporal/efti_vc_{}.js'

def timing_table(algo):
    fn = algo_js_tmplt.format(algo)
    make_feature_comp_tables([fn], ['time'], algo, horizontal_splits=3, titles=None,
                             head_fmt=r":raw:`\multicolumn{{1}}{{c}}{{Ind. Time [s]}}`",
                             data_fmt=r':math:`{0:0.2f} \pm {1:04.2f}`')

number_formats = {
    'size': r':math:`{0:0.1f} \pm {1:>5.1f}`',
    'acc': r':math:`{0:0.2f}`',
    'fit': r':math:`{0:0.2f} \pm {1:>4.2f}`'
}

def acc_size_compare_table(algo, algo_name, cw):
    algo_fn = algo_js_tmplt.format(algo)
    efti_fn = efti_compare_js_tmplt.format(algo)

    data, cvs = load_data([algo_fn, efti_fn], cw)
    tables = {}
    csv_table_prep = {}
    for f in ['acc', 'size', 'fit']:
        tables[f] = form_mean_table(data[f])

        if f == 'acc':
            for ds in tables[f]:
                for a in tables[f][ds]:
                    tables[f][ds][a] = tuple(v*100 for v in tables[f][ds][a])

        csv_table_prep[f] = prepare_csv_table(tables[f], cvs,
                                              sort_by_desc=False,
                                              head_fmt=r":raw:`\multicolumn{{1}}{{c}}{{{}}}`",
                                              data_fmt=number_formats[f]
                                              )

    csv_table = []
    csv_table.append(
        ['',
         r":raw:`\multicolumn{2}{c|}{Accuracy}`",
         r":raw:`\multicolumn{2}{c|}{Size}`",
         r":raw:`\multicolumn{2}{c}{Fitness}`"
         ]
        )
    csv_table.append(
        ['Dataset',
         r":raw:`\multicolumn{1}{c}{" + algo_name + "}`", r":raw:`\multicolumn{1}{c|}{EFTI}`",
         r":raw:`\multicolumn{1}{c}{" + algo_name + "}`", r":raw:`\multicolumn{1}{c|}{EFTI}`",
         r":raw:`\multicolumn{1}{c}{" + algo_name + "}`", r":raw:`\multicolumn{1}{c}{EFTI}`"
         ]
        )

    for a, s, c in zip(csv_table_prep['acc'][1:],
                       csv_table_prep['size'][1:],
                       csv_table_prep['fit'][1:]):
        ds = a[0]
        row = [ds]
        for f, optim, orig_row in zip(['acc', 'size', 'fit'],
                                      [lambda x: x, lambda x: not x, lambda x: x], [a, s, c]):
            algo_val = tables[f][ds][0][0]
            efti_val = tables[f][ds][1][0]

            if optim(algo_val > efti_val):
                reldif = abs(algo_val - efti_val)/algo_val
                color = 'carnelian'
                cmax = 60
            else:
                reldif = abs(efti_val - algo_val)/efti_val
                color = 'bluegray'
                cmax = 80

            if f == 'size':
                alpha = int(cmax*(1 - math.exp(-reldif)))
            else:
                alpha = int(cmax*(1 - math.exp(-reldif/0.1)))

            # print(ds, reldif, alpha)
            # else:
            #     if reldif > 0.7:
            #         reldif = 0.7
            #     alpha = int(reldif*100)

            ltx = r':raw:`\cellcolor{{{}!{}}}`'.format(color,alpha)
            row.extend([ltx + orig_row[1], ltx + orig_row[2]])

        csv_table.append(row)

    write_csv_table('{}-comp.csv'.format(algo), csv_table)

if __name__ == "__main__":
    timing_table(sys.argv[1])
    acc_size_compare_table(sys.argv[1], sys.argv[2], float(sys.argv[3]))
