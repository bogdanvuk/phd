import sys
import os
import numpy as np
sys.path.append(os.path.expandvars('$EFTI/script'))
from rank import load_data, form_mean_table, dump_table_csv
import matplotlib.pyplot as plt
import matplotlib
from plot_tools import form_clusters
from subfig_tools import substitute_subfigure, subfig_tmpl, fig_tmpl

def form_cluster_matrix(table):
    m = []
    for ds in sorted(table):
        m.append([table[ds][k][0] for k in table[ds]])

    return np.matrix(m)

def print_figures(table, feature, fplot, xvals, name, loc=1, figs=None):
    plots = form_cluster_matrix(table)

    if figs is None:
        figs = [[j for j in range(i,i+5)] for i in range(0,50,5)]

    line_styles = ['-', '--', ':', '-', '--']
    line_widths = [2,2,2,4,4]
    for n,f in enumerate(figs):
        plt.close()
        w, h = matplotlib.figure.figaspect(0.6)
        fig = plt.figure(figsize=(w,h))
        legend_handle = []
        legend_title = []

        for i,p in enumerate(f):
            # plt.semilogy([0, 0.01, 0.02, 0.06, 0.1], plots[i].A1)
            legend_title.append(list(sorted(table))[p])
            line, = fplot(
                xvals,
                plots[p].A1,
                linewidth=line_widths[i],
                linestyle=line_styles[i]
            )

            legend_handle.append(line)

        # plt.gca().set_aspect(0.7)
        # forceAspect(plt.gca(), 0.7)
        plt.gca().legend(legend_handle, legend_title, loc=loc)
        plt.tight_layout()
        plt.savefig("../images/{}/{}{}.pdf".format(name,feature,n), bbox_inches='tight')

def make_feature_comp_tables(files, features, name, horizontal_splits=1, titles=None,
                             head_fmt=r":raw:`\multicolumn{{1}}{{c}}{{{}}}`",
                             data_fmt="{0:0.2f}"):
    data, cvs = load_data(files, 0.02)
    if titles:
        for i, n in enumerate(titles):
            cvs[i]['desc'] = n

    for feature in features:
        table = form_mean_table(data[feature])

        dump_table_csv("{}-{}.csv".format(name, feature),
                       table, cvs, horizontal_splits=horizontal_splits,
                       sort_by_desc=False, head_fmt=head_fmt, data_fmt=data_fmt)

def table_fig_dual_feature(files, features, name, rst_file, xvals, fignum=10, fig_plotsnum=5,
                           cluster_by=None, plot_funcs=(plt.plot, plt.plot),
                           subfig_caption = "DT {feature}: {datasets}",
                           fig_caption = "{name}", titles=None, locs=["lower left", "lower left"]
                           ):
    if (cluster_by is None) or (features[0] == cluster_by):
        fig_order = features
    else:
        fig_order = list(reversed(features))
        plot_funcs = list(reversed(plot_funcs))
        locs = list(reversed(locs))

    data, cvs = load_data(files, 0.02)

    if titles:
        for i, n in enumerate(titles):
            cvs[i]['desc'] = n

    for feature, plot, l in zip(fig_order, plot_funcs, locs):
        table = form_mean_table(data[feature])
        plots = form_cluster_matrix(table)
        if feature == cluster_by:
            figs = form_clusters(plots,fignum,fig_plotsnum)

        print_figures(table,feature, plot, xvals=xvals, name=name, loc=l, figs=figs)
        dump_table_csv("{}-{}.csv".format(name, feature),
                       table, cvs, variance=False, sort_by_desc=False)

    subfigs = []
    for i,f in enumerate(figs):
        for feature in features:
            datasets = ', '.join([list(sorted(table))[p] for p in f])
            subfigs.append(subfig_tmpl.format(name=name,
                                              feature=feature,
                                              id=i,
                                              caption=subfig_caption.format(feature=feature,
                                                                            datasets=datasets)
            ))

    for i in range(2):
        figure = fig_tmpl.format(name=name + str(i+1),
                                 subfigures=''.join(subfigs[i*10:(i+1)*10]),
                                 caption=fig_caption.format(name=name))
        substitute_subfigure(rst_file, figure, name + str(i+1))
