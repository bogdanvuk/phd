import sys
import os

os.environ['EFTI'] = '/data/projects/efti'
sys.path.append(os.path.expandvars('$EFTI/script'))
from rank import load_data, form_mean_table, dump_table_csv, rank

files = [
    'EFTI_500k.js',
    # 'EFTI_500k_norp.js',
    'EFTI_500k_nosp.js',
]

files = [os.path.join('results', f) for f in files]
rank(files, 0.02)
# data, cvs = load_data(files, 0.02)

# cvs[0]['desc'] = "Standard"
# cvs[1]['desc'] = "No return to best"
# cvs[2]['desc'] = "No search probability"

# table = form_mean_table(data['fit'])
# dump_table_csv("no_search_comp_fit.csv", table, cvs, variance=True, sort_by_desc=False)
