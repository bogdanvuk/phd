import sys
import os
sys.path.append(os.path.expandvars('$EFTI/script'))
from efti_intf import spawn, EftiCmdBase
import logging

max_iter = 30000
param_def = {
    'max_iter': max_iter,
    'ensemble_size': 1,
    'oversize_w': 0.02,
    'dataset_selection': 'jvow',
    'search_prob': 0,
    's_accel_stagn': 0,
    'w_accel_stagn': 0.001,
    't_accel_stagn': 0.0,
    'weight_mut': 0.0,
    'seed': 1205,
    'runs': 1,
    'folds': 1,
    'return_prob': 0
}

def run_sim(jsfn, params):
    logging.basicConfig(format='%(asctime)s %(message)s', stream=sys.stdout, level = logging.DEBUG)
    if os.path.exists(jsfn):
        os.remove(jsfn)
    spawn(EftiCmdBase(jsfn), path=os.path.expandvars('$EFTI/rel/efti'), params=[params], name='w0')

runs = [
    {"fn": '../data/searchprob/jvow_fitpath_vanilla.js', "params": {
        'search_function': 0}
    },
    {"fn": '../data/searchprob/jvow_fitpath_hereboy.js', "params": {
        'search_prob': 1e-3,
        'search_function': 2}
    }
    ]

for r in runs:
    params = param_def.copy()
    params.update(r['params'])
    run_sim(r['fn'], params)
