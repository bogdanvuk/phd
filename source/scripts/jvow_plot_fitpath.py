sys.path.append(os.path.expandvars('$EFTI/script'))
from efti_intf import spawn, EftiCmdBase
import os
import sys
import logging

max_iter = 500000
param_def = {
    'max_iter': max_iter,
    'ensemble_size': 1,
    'oversize_w': 0.02,
    'dataset_selection': 'jvow',
    'search_prob': 0,
    'w_accel_stagn': 0.001,
    't_accel_stagn': 0.0,
    'weight_mut': 0.0,
    'runs': 1,
    'folds': 1,
}

def run_sim(jsfn, params):
    logging.basicConfig(format='%(asctime)s %(message)s', stream=sys.stdout, level = logging.DEBUG)
    if os.path.exists(jsfn):
        os.remove(jsfn)
    spawn(EftiCmdBase(jsfn), path=os.path.expandvars('$EFTI/rel/efti'), params=[params], name='w0')

runs = [
    # {"fn": 'fitpath_full.js', "params": {
    #     's_accel_stagn': 5e-5,
    #     'return_prob': 0.0001}
    # },
    {"fn": '../data/searchprob/jvow_fitpath_bare.js', "params": {
        's_accel_stagn': 0,
        'return_prob': 0}
    },
    {"fn": '../data/searchprob/jvow_fitpath_norp.js', "params": {
        's_accel_stagn': 5e-5,
        'return_prob': 0}
    }
    ]

for r in runs:
    params = param_def.copy()
    params.update(r['params'])
    run_sim(r['fn'], params)
