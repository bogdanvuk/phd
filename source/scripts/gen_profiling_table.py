from subprocess import call
import sys
import os
sys.path.append(os.path.expandvars('$EFTI/script'))
from rank import load_js_data, dump_table_csv, prepare_csv_table, write_csv_table, features, form_mean_table, form_mean_rank, anova
import json
import os
import csv

files_all = ['adult', 'ausc', 'bank', 'bc', 'bch', 'bcw', 'ca', 'car', 'cmc', 'ctg', 'cvf', 'eb', 'eye', 'ger', 'gls', 'hep', 'hrtc', 'hrts', 'ion', 'irs', 'jvow', 'krkopt', 'letter', 'liv', 'lym', 'magic', 'msh', 'nurse', 'page', 'pen', 'pid', 'psd', 'sb', 'seg', 'shuttle', 'sick', 'son', 'spect', 'spf', 'thy', 'ttt', 'veh', 'vene', 'vote', 'vow', 'w21', 'w40', 'wfr', 'wilt', 'wine', 'zoo']

param_def = {
    'max_iter': 10000,
    'ensemble_size': 1,
    'oversize_w': 0.02,
    # 'dataset_selection': ','.join(sorted(files_all)),
    'search_prob': 0,
    's_accel_stagn': 0.0,
    't_accel_stagn': 0.0,
    'w_accel_stagn': 0.0,
    'return_prob': 0,
    'weight_mut': 0.0,
    'topo_mut': 0.0,
    'runs': 1,
}

funcs = ['find_dt_leaf_for_inst',
         'accuracy_calc',
         'evaluate_node_test',
         'apply_single_path_change',
         'others']

gprof_row_tmplt = {f:0 for f in funcs}

def load_gprof_for_file():
    cmd_line = ' '.join(['gprof', '-b', os.path.expandvars('$EFTI/rel/efti'), 'gmon.out', '>', 'gmon.txt'])
    call(cmd_line, shell=True)
    row = gprof_row_tmplt.copy()
    with open('gmon.txt') as f:
        lines = f.readlines()
        for line in lines[5:]:
            if not "clone" in line:
                gprof_row = line.partition('(')[0].split()
                if gprof_row:
                    if gprof_row[-1] in row:
                        row[gprof_row[-1]] = float(gprof_row[0]) / 100
                else:
                    break

    total = sum(row.values())
    row['others'] = abs(1 - total)
    return row

# def dump_csv(fn, table):
#     with open(fn, 'w', newline='') as csvfile:

#         csvwriter = csv.writer(csvfile, delimiter=',',
#                            quotechar='"', quoting=csv.QUOTE_MINIMAL)

#         head_row = ['Dataset'] + funcs
#         csvwriter.writerow(head_row)

#         for d,res in iter(sorted(table.items())):
#             row = [d] + ["{0:2.1f}".format(res[f]*100) for f in funcs]
#             csvwriter.writerow(row)

def gprof():
    table = {}

    for f in files_all:
        cmd_line = [os.path.expandvars('$EFTI/rel/efti')]
        for k,v in param_def.items():
            cmd_line.append('--{}={}'.format(k,v))

        cmd_line.append('--{}={}'.format('dataset_selection', f))
        cmd_line = ' '.join(cmd_line)
        print(cmd_line)
        call(cmd_line, shell=True)

        table[f] = load_gprof_for_file()

        with open('profiling.js', 'w') as fp:
            json.dump(table, fp)

    return table

short_name = [
    'FDLFI',
    'AC',
    'ENT',
    'ASPC',
    'Others'
]
def dump_gprof_table_csv(fn):
    table = load_js_data('profiling.js')

    cvs = {}
    for i,n in enumerate(short_name):
        cvs[i] = {'desc': '{} [%]'.format(n)}

    mean_perc = {k:0 for k in funcs}
    table_hack = {}
    for ds in table:
        if ds not in table_hack:
            table_hack[ds] = {}

        for i,f in enumerate(funcs):
            table_hack[ds][i] = table[ds][f] * 100
            mean_perc[f] += table[ds][f] * 100

    for f in funcs:
        mean_perc[f] /= len(table)


    csv_table = prepare_csv_table(
        table_hack, cvs,
        sort_by_desc=False,
        data_fmt="{0:0.2f}"
    )

    csv_table.append([r":raw:`\bottomrule \renewcommand{\arraystretch}{0.8} average`"] + ['{:0.2f}'.format(mean_perc[f]) for f in funcs])
    write_csv_table("profiling.csv", csv_table)

# table = gprof()
# table = load_js_data('profiling.js')
dump_gprof_table_csv('profiling.csv')
