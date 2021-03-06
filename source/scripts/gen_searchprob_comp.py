import sys
import os
sys.path.append(os.path.expandvars('$EFTI/script'))
from rank import load_js_data, mean_confidence_interval
from rank import anova, load_data, form_mean_table, prepare_csv_table, write_csv_table, dump_table_csv, form_mean_rank
from table_fig_dual_feature import make_feature_comp_tables

files = [
    'EFTI_500k_ow-0.01_nosp.js',
    'EFTI_500k_hereboy_searchprob.js',
    'EFTI_500k_ow-0.01_norp.js',
    'EFTI_500k_ow-0.01.js',
]

files = [os.path.join('results', f) for f in files]
titles = ['Greedy', r'Hereboy', r'Metropolis', r'Metropolis with restarts']
fmt_titles = [
    r":raw:`\multicolumn{2}{c|}{Greedy}`",
    r":raw:`\multicolumn{2}{c|}{Hereboy}`",
    r":raw:`\multicolumn{2}{c|}{Metropolis}`",
    r':raw:`\multicolumn{2}{>{\centering\arraybackslash}m{32mm}}{Metropolis with restarts}`',
]
# make_feature_comp_tables(files, ['fit'], 'searchprob-comp', horizontal_splits=1, titles=titles,
#                          head_fmt=r':raw:`\multicolumn{{1}}{{>{{\centering\arraybackslash}}m{{32mm}}}}{{{}}}`',
#                          data_fmt=r':math:`{0:0.3f} \pm {1:05.3f}`')

# make_feature_comp_tables(files, ['fit'], 'searchprob-comp', horizontal_splits=2, titles=titles,
#                          head_fmt=r':raw:`\multicolumn{{1}}{{>{{\centering\arraybackslash}}m{{32mm}}}}{{{}}}`',
#                          data_fmt=r':math:`{0}`')

def fit_compare_table(cw):
    data, cvs = load_data(files, cw)
    tables = {}
    csv_table_prep = {}
    table = form_mean_table(data['fit'])
    rank = anova(data['fit'], True)

    csv_table_prep = prepare_csv_table(table, cvs,
                                       sort_by_desc=False,
                                       head_fmt=r":raw:`\multicolumn{{1}}{{c}}{{{}}}`",
                                       data_fmt=r':math:`{0:0.3f} \pm {1:05.3f}`'
    )

    csv_rank_prep = prepare_csv_table(rank, cvs,
                                       sort_by_desc=False,
                                       head_fmt=r":raw:`\multicolumn{{1}}{{c}}{{{}}}`",
                                       data_fmt=r':raw:`{0}`'
    )

    csv_table = []
    csv_table.append([''] + fmt_titles)
    csv_table.append(
        ['Dataset',
         r":raw:`\multicolumn{1}{c}{\footnotesize Fitness}`", r":raw:`\multicolumn{1}{c|}{\footnotesize Rank}`",
         r":raw:`\multicolumn{1}{c}{\footnotesize Fitness}`", r":raw:`\multicolumn{1}{c|}{\footnotesize Rank}`",
         r":raw:`\multicolumn{1}{c}{\footnotesize Fitness}`", r":raw:`\multicolumn{1}{c|}{\footnotesize Rank}`",
         r":raw:`\multicolumn{1}{c}{\footnotesize Fitness}`", r":raw:`\multicolumn{1}{c}{\footnotesize Rank}`",
         ]
        )

    # csv_rank_prep.insert(3, ['bank', '0', '0', '0', '0'])
    # csv_rank_prep.insert(35, ['shuttle', '0', '0', '0', '0'])
    for frow, rrow in zip(csv_table_prep[1:],
                          csv_rank_prep[1:]):
        assert frow[0] == rrow[0]
        ds = frow[0]
        row = [ds]

        for f, r in zip(frow[1:], rrow[1:]):
            row += [f, r]

        csv_table.append(row)

    mean_rank = form_mean_rank(rank)
    csv_table.append([r":raw:`\bottomrule rank`"] + [r":raw:`\multicolumn{{2}}{{c|}}{{{:.2f}}}`".format(mean_rank[c]) for c in cvs])
    # print(csv_table[-1][-1])
    csv_table[-1][-1] = csv_table[-1][-1].replace('{c|}', '{c}')
    # print(csv_table[-1][-1])

    write_csv_table('searchprob-comp-fit.csv', csv_table)

    # mean_rank = form_mean_rank(rank)
    # print(mean_rank)
    # csv_table = [fmt_titles]
    # csv_table.append(['{:.2f}'.format(mean_rank[c]) for c in cvs])
    # write_csv_table('searchprob-comp-mean-ranks.csv', csv_table)

fit_compare_table(0.01)
