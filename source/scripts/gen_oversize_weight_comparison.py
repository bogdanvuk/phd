import sys
import os
import numpy as np
from sklearn.cluster import KMeans
sys.path.append(os.path.expandvars('$EFTI/script'))
from rank import load_data, form_mean_table, dump_table_csv
import matplotlib.pyplot as plt
import matplotlib

def form_cluster_matrix(table):
    m = []
    for ds in sorted(table):
        m.append([table[ds][k][0] for k in table[ds]])

    return np.matrix(m)

def form_clusters(plots, fignum, fig_plotsnum):
    estim = KMeans(n_clusters=fignum)
    estim.fit(plots)
    clusters = {i:l for i,l in enumerate(estim.labels_)}

    figs = [[] for f in range(fignum)]

    for f in range(fignum):
        for i in list(clusters.keys()):
            if f >= clusters[i]:
                figs[f].append(i)
                del clusters[i]
                if len(figs[f]) == fig_plotsnum:
                    break

    return figs

def print_figures(fignum, fig_plotsnum, table, feature, fplot, loc=1, figs=None):
    plots = form_cluster_matrix(table)

    if figs is None:
        figs = [[j for j in range(i,i+5)] for i in range(0,50,5)]

    line_styles = ['-', '--', ':', '-', '--']
    line_widths = [2,2,2,4,4]
    for f in range(fignum):
        plt.close()
        fig = plt.figure()
        legend_handle = []
        legend_title = []

        for i,p in enumerate(figs[f]):
            # plt.semilogy([0, 0.01, 0.02, 0.06, 0.1], plots[i].A1)
            legend_title.append(list(sorted(table))[p])
            line, = fplot(
                [0.0001, 0.01, 0.02, 0.06, 0.1],
                plots[p].A1,
                linewidth=line_widths[i],
                linestyle=line_styles[i]
            )

            legend_handle.append(line)

        fig.legend(legend_handle, legend_title, loc=loc)
        plt.tight_layout()
        plt.savefig("../images/oversize_compare/{}{}.pdf".format(feature,f), bbox_inches='tight')

def substitute_subfigure(file, subfig):
    with open('../efti.rst', 'r') as f:
        data = f.read()

    endpos = data.find('fig-oversize-compare')
    # Get to the end of the subfigure
    for _ in range(3):
        endpos = data.find('\n', endpos)

    # Find beggining of the subfigure
    startpos = data.find('.. subfigstart::', 0, endpos)

    data = data[:strpos] + subfig + data[endpos:]

    with open('./myfile', 'w') as f:
        for line in lines:
            line = line.replace('word', 'new')
            f.write(line)

files = [
    'EFTI_500k_ow-0.0.js',
    'EFTI_500k_ow-0.01.js',
    'EFTI_500k.js',
    'EFTI_500k_ow-0.06.js',
    'EFTI_500k_ow-0.1.js',
]

files = [os.path.join('results', f) for f in files]

os.environ['EFTI'] = '/data/projects/efti'
data, cvs = load_data(files, 0.02)

for i, n in enumerate(["0.0", "0.01", "0.02", "0.06", "0.1"]):
    cvs[i]['desc'] = n

fignum = 10
fig_plotsnum = 5

# plt.gca().set_xticks(["0.0001"fd, 0.01, 0.02, 0.06, 0.1])
# plt.gca().get_xaxis().get_major_formatter().labelOnlyBase = False
# plt.gca().get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
# plt.gca().set_ylim(2, max([plots[i].A1[0] for i in figs[9]]))
# plt.show()
# print(figs)

table = form_mean_table(data['acc'])
plots = form_cluster_matrix(table)
figs = form_clusters(plots,fignum,fig_plotsnum)
# print_figures(fignum, fig_plotsnum, table, 'acc', plt.semilogx, loc="upper right", figs=figs)
# dump_table_csv("oversize_weight_acc_comp.csv", table, cvs, variance=False, sort_by_desc=False)

# table = form_mean_table(data['size'])
# print_figures(fignum, fig_plotsnum, table, 'size', plt.loglog, loc="upper right", figs=figs)
# dump_table_csv("oversize_weight_size_comp.csv", table, cvs, variance=False, sort_by_desc=False)

subfig_tmpl = """
.. _fig-oversize-compare-{feature}{id}:

.. figure:: images/oversize_compare/{feature}{id}.pdf
    :align: center

    DT {feature}: {datasets}
"""

fig_tmpl = """
.. subfigstart::
{subfigures}
.. subfigend::
    :width: 0.48
    :label: fig-oversize-compare

    The figure shows the dependencies of the DT sizes and accuracies on the oversize weight (|Ko|) parameter values. DT sizes and accuracies are displayed for five datasets per subfigure.
"""
subfigs = []
for i,f in enumerate(figs):
    for feature in ['size', 'acc']:
        datasets = ', '.join([list(sorted(table))[p] for p in f])
        subfigs.append(subfig_tmpl.format(feature=feature, id=i, datasets=datasets))

figure = fig_tmpl.format(subfigures=''.join(subfigs))
print(figure)
# substitute_subfigure('../efti.rst', figure)
