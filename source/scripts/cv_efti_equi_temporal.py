#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.expandvars('$EFTI/script'))
from rank import load_data, mean_confidence_interval
from efti_intf import efti_test

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

if __name__ == "__main__":
    run_equitemporal(sys.argv[1])
