import sys
import os
sys.path.append('../../../efti/script')
from rank import load_data, form_mean_table, dump_table_csv

files = [
    'EFTI_500k_ow-0.0.js',
    'EFTI_500k.js',
    'EFTI_500k_ow-0.06.js',
    'EFTI_500k_ow-0.1.js',
]

files = [os.path.join('results', f) for f in files]

os.environ['EFTI'] = '/data/projects/efti'
data, cvs = load_data(files, 0.02)

for i, n in enumerate(["0.0", "0.02", "0.06", "0.1"]):
    cvs[i]['desc'] = n

table = form_mean_table(data['size'])
dump_table_csv("oversize_weight_size_comp.csv", table, cvs, variance=True)
table = form_mean_table(data['acc'])
dump_table_csv("oversize_weight_acc_comp.csv", table, cvs, variance=True)
