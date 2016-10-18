#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.expandvars('$EFTI/script'))
from rank import load_data, dump_table_csv, prepare_csv_table, write_csv_table, features, form_mean_table, form_mean_rank, anova

files = [
    'oc1_ap.js',
    'cart.js',
    'oc1.js',
    'oc1_es.js',
    'oc1_sa.js',
    'nodt.js',
    'gale.js',
    'gatree.js',
    'EFTI_1000k_ow-0.01.js'
]

files = [os.path.join('results', f) for f in files]
titles = ['OC1-AP', r'CART-LC', r'OC1', r'OC1-ES', r'OC1-SA', r'NODT', 'GALE', 'GaTree', 'EFTI']
titles_perc = [r'OC1-AP \ [\%]', r'CART-LC \ [\%]', r'OC1 \ [\%]', r'OC1-ES \ [\%]', r'OC1-SA \ [\%]', r'NODT \ [\%]', r'GALE \ [\%]', r'GaTree \ [\%]', r'EFTI \ [\%]']
number_formats = {
    'size': (r':math:`{0:0.1f}`', r":math:`\pm {1:0.1f}`"),
    'acc': (r':math:`{0:0.2f}`', r":math:`\pm {1:0.2f}`")
}

# head_fmt=r':raw:`\multicolumn{{1}}{{>{{\centering\arraybackslash}}p{{16mm}}}}{{{}}}`'
head_fmt=r":raw:`\multicolumn{{1}}{{c}}{{{}}}`"

def derive_relative_table(table, ref):
    table_rel = {}
    for ds in table:
        table_rel[ds] = {}
        val_max = table[ds][ref][0]
        for algo, val in table[ds].items():
            if algo != ref:
                table_rel[ds][algo] = (val[0] - val_max)/val_max*100

    return table_rel

def gen_tables(files, cw, titles=None):
    data, cvs = load_data(files, cw)
    if titles:
        for i, n in enumerate(titles):
            cvs[i]['desc'] = n

    cvs_no_efti = {k:v for k,v in cvs.items() if k != (len(files) - 1)}
    mean_ranks = {}
    for f in [fe for fe in features if fe not in ['time', 'fit']]:
        table = form_mean_table(data[f])
        if f == 'acc':
            for ds in table:
                for a in table[ds]:
                    table[ds][a] = tuple(v*100 for v in table[ds][a])

        dump_table_csv("comp-mean-{}-{}.csv".format(f, cw),
                       table, cvs,
                       sort_by_desc=False,
                       dstitle='',
                       head_fmt=head_fmt,
                       data_fmt=number_formats[f][0]
                       )

        dump_table_csv("comp-conf-{}-{}.csv".format(f, cw),
                       table, cvs,
                       sort_by_desc=False,
                       dstitle='',
                       head_fmt=head_fmt,
                       data_fmt=number_formats[f][1]
                       )

        table_rel = derive_relative_table(table, len(files)-1)
        dump_table_csv("comp-mean-relative-{}-{}.csv".format(f,cw),
                       table_rel, cvs_no_efti,
                       dstitle='',
                       sort_by_desc=False,
                       data_fmt=number_formats[f][0],
                       head_fmt=head_fmt,
                       )

        rank = anova(data[f], features[f]['desc'])

        csv_table = prepare_csv_table(
            rank, cvs,
            sort_by_desc=False,
            dstitle='',
            head_fmt=head_fmt,
            data_fmt=r":math:`{}`"
        )

        mean_rank = form_mean_rank(rank)
        csv_table.append([r":raw:`\bottomrule rank`"] + ['{:0.3f}'.format(mean_rank[c]) for c in cvs])
        write_csv_table("comp-rank-{}-{}.csv".format(f,cw), csv_table)

        # mean_ranks[f] = form_mean_rank(rank)

    # dump_mean_sorted_ranks("mean_ranks.csv", mean_ranks, cvs)

if __name__ == "__main__":
    gen_tables(files, float(sys.argv[1]), titles)
