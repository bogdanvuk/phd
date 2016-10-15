import sys
import os
sys.path.append(os.path.expandvars('$EFTI/script'))
from efti_intf import spawn, EftiCmdBase
import logging

param_def = {
    'max_iter': 15000,
    'ensemble_size': 1,
    'oversize_w': 0.01,
    'dataset_selection': 'veh',
    'w_accel_stagn': 0.0,
    's_accel_stagn': 5e-5,
    'search_prob': 0.05,
    'search_function': 1,
    'return_prob': 0,
    'weight_mut': 0,
    'topo_mut': 0.6,
    't_accel_stagn': 1,
    'folds': 1,
    'runs': 1
}

def run_sim(jsfn, params):
    logging.basicConfig(format='%(asctime)s %(message)s', stream=sys.stdout, level = logging.DEBUG)
    if os.path.exists(jsfn):
        os.remove(jsfn)
    spawn(EftiCmdBase(jsfn), path=os.path.expandvars('$EFTI/rel/efti'), params=[params], name='w0')

runs = [
    {"fn": '../data/searchprob/veh_fitpath_vanilla.js', "params": {
        'search_function': 0}
    },
    {"fn": '../data/searchprob/veh_fitpath_metropolis.js', "params": {
        'return_prob': 0}
    },
    {"fn": '../data/searchprob/veh_fitpath_metropolis_rp.js', "params": {
        'return_prob': 0.0005}
    },
    {"fn": '../data/searchprob/veh_fitpath_hereboy.js', "params": {
        'search_prob': 2e-3,
        'search_function': 2}
    }
    ]

for r in runs:
    params = param_def.copy()
    params.update(r['params'])
    run_sim(r['fn'], params)
