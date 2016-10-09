#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.expandvars('$EFTI/script'))
from rank import load_js_data, mean_confidence_interval
from efti_intf import efti_test
from rank import load_data, form_mean_table, prepare_csv_table, write_csv_table
from table_fig_dual_feature import make_feature_comp_tables
import math

files_all = ['adult', 'ausc', 'bank', 'bc', 'bch', 'bcw', 'ca', 'car', 'cmc', 'ctg', 'cvf', 'eb', 'eye', 'ger', 'gls', 'hep', 'hrtc', 'hrts', 'ion', 'irs', 'jvow', 'krkopt', 'letter', 'liv', 'lym', 'magic', 'msh', 'nurse', 'page', 'pen', 'pid', 'psd', 'sb', 'seg', 'shuttle', 'sick', 'son', 'spect', 'spf', 'thy', 'ttt', 'veh', 'vene', 'vote', 'vow', 'w21', 'w40', 'wfr', 'wilt', 'wine', 'zoo']

param_def = {
    'max_iter': 500000,
    'ensemble_size': 1,
    'oversize_w': 0.001,
    'w_accel_stagn': 0.0,
    's_accel_stagn': 5e-5,
    'search_prob': 0.05,
    'search_function': 1,
    'return_prob': 0.0001
}

algo_js_tmplt = 'results/equi_temporal/{}.js'
efti_compare_js_tmplt = 'results/equi_temporal/efti_vc_{}.js'

def load_algo_data(algo):
    fn = algo_js_tmplt.format(algo)
    data, cvs = load_data([fn], 0.02)

    return data, cvs

def run_equitemporal(algo):
    data, cvs = load_algo_data(algo)
    logfn = efti_compare_js_tmplt.format(algo)
    if os.path.exists(logfn):
        os.remove(logfn)

    for ds in sorted(files_all):
        test_set = {'log': logfn, 'conf': []}
        p = param_def.copy()
        p['dataset_selection'] = ds
        p['max_time'] = mean_confidence_interval(data['time'][ds][0])[0]
        test_set['conf'].append(p)

        print("Running test for {} in {} time".format(ds, p['max_time']))
        efti_test(path=os.path.expandvars('$EFTI/rel/efti'), threads=0, tests=[test_set])

def timing_table(algo):
    fn = algo_js_tmplt.format(algo)
    make_feature_comp_tables([fn], ['time'], algo, horizontal_splits=3, titles=None,
                             head_fmt=r":raw:`\multicolumn{{1}}{{c}}{{Ind. Time [s]}}`",
                             data_fmt=r':math:`{0:0.3f} \pm {1:05.3f}`')

def acc_compare_table(algo):
    algo_fn = algo_js_tmplt.format(algo)
    efti_fn = efti_compare_js_tmplt.format(algo)

    make_feature_comp_tables([algo_fn, efti_fn], ['acc'], 'cart-comp',
                             horizontal_splits=2, titles=None,
                             head_fmt=r":raw:`\multicolumn{{1}}{{c}}{{{}}}`",
                             data_fmt=r':math:`{0:0.2f} \pm {1:05.3f}`')

# acc_compare_table('cart')

number_formats = {
    'size': r':math:`{0:0.1f} \pm {1:>5.1f}`',
    'acc': r':math:`{0:0.2f} \pm {1:04.2f}`',
    'fit': r':math:`{0:0.2f} \pm {1:>4.2f}`'
}

def acc_size_compare_table(algo, cw):
    algo_fn = algo_js_tmplt.format(algo)
    efti_fn = efti_compare_js_tmplt.format(algo)

    data, cvs = load_data([algo_fn, efti_fn], cw)
    tables = {}
    csv_table_prep = {}
    for f in ['acc', 'size', 'fit']:
        tables[f] = form_mean_table(data[f])
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
         r":raw:`\multicolumn{1}{c}{CART-LC}`", r":raw:`\multicolumn{1}{c|}{EFTI}`",
         r":raw:`\multicolumn{1}{c}{CART-LC}`", r":raw:`\multicolumn{1}{c|}{EFTI}`",
         r":raw:`\multicolumn{1}{c}{CART-LC}`", r":raw:`\multicolumn{1}{c}{EFTI}`"
         ]
        )

    for a, s, c in zip(csv_table_prep['acc'][1:],
                       csv_table_prep['size'][1:],
                       csv_table_prep['fit'][1:]):
        ds = a[0]
        row = [ds]
        for f, optim, orig_row in zip(['acc', 'size', 'fit'],
                                      [lambda x: x, lambda x: not x, lambda x: x], [a, s, c]):
            algo = tables[f][ds][0][0]
            efti = tables[f][ds][1][0]

            if optim(algo > efti):
                reldif = abs(algo - efti)/algo
                color = 'carnelian'
            else:
                reldif = abs(efti - algo)/efti
                color = 'bluegray'

            # if f == 'acc':
            alpha = int(80*(1 - math.exp(-reldif/0.1)))
            # print(ds, reldif, alpha)
            # else:
            #     if reldif > 0.7:
            #         reldif = 0.7
            #     alpha = int(reldif*100)

            ltx = r':raw:`\cellcolor{{{}!{}}}`'.format(color,alpha)
            row.extend([ltx + orig_row[1], ltx + orig_row[2]])

        csv_table.append(row)

    # print(csv_table)
    write_csv_table('cart-acc-size-comp.csv', csv_table)
    # print(csv_table)

# acc_size_compare_table('cart', 0.001)

if __name__ == "__main__":
    run_equitemporal(sys.argv[1])
    # acc_size_compare_table('cart', 0.001)
    # acc_compare_table('cart')

# def timing_table(algo):
#     data = load_data(algo)
# def make_feature_comp_tables(files, features, name, horizontal_splits=1, titles=None,
#                              head_fmt=r":raw:`\multicolumn{{1}}{{c}}{{{}}}`",
#                              data_fmt="{0:0.2f}"):

#     data, cvs = load_data(files, 0.02)
#     if titles:
#         for i, n in enumerate(titles):
#             cvs[i]['desc'] = n

#     for feature in features:
#         table = form_mean_table(data[feature])

#         dump_table_csv("{}-{}.csv".format(name, feature),
#                        table, cvs, horizontal_splits=horizontal_splits,
#                        sort_by_desc=False, head_fmt=head_fmt, data_fmt=data_fmt)


# data, cvs = load_algo_data('cart', 0.02)
# table = form_mean_table(data['time'])
# dump_table_csv("{}-{}.csv".format('cart', 'time'),
#                table, cvs, horizontal_splits=3,
#                sort_by_desc=False, head_fmt=head_fmt, data_fmt=data_fmt)

# print(table)
