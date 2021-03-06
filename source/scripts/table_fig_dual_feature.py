import sys
import os
import numpy as np
sys.path.append(os.path.expandvars('$EFTI/script'))
from rank import load_data, form_mean_rank, form_mean_table, dump_table_csv, prepare_csv_table, write_csv_table
from rank import features as feature_properties, anova
import matplotlib.pyplot as plt
import matplotlib
from plot_tools import form_clusters
from subfig_tools import substitute_subfigure, subfig_tmpl, fig_tmpl

def form_cluster_matrix(table):
    m = []
    for ds in sorted(table):
        m.append([table[ds][k][0] for k in table[ds]])

    return np.matrix(m)

def print_figures(table, feature, fplot, xvals, name, loc=1, figs=None, aspect=1):
    plots = form_cluster_matrix(table)

    if figs is None:
        figs = [[j for j in range(i,i+5)] for i in range(0,50,5)]

    line_styles = ['-', '--', ':', '-', '--']
    line_widths = [8,8,8,8,8]
    for n,f in enumerate(figs):
        plt.close()
        w, h = matplotlib.figure.figaspect(aspect)
        fig = plt.figure(figsize=(w,h))
        legend_handle = []
        legend_title = []

        for i,p in enumerate(f):
            # plt.semilogy([0, 0.01, 0.02, 0.06, 0.1], plots[i].A1)
            if isinstance(p,str):
                ds = p
                ds_id = sorted(table).index(p)
            else:
                ds_id = p
                ds = sorted(table)[p]

            legend_title.append(ds)
            line, = fplot(
                xvals,
                plots[ds_id].A1,
                linewidth=line_widths[i],
                linestyle=line_styles[i]
            )

            legend_handle.append(line)

        # plt.gca().set_aspect(0.7)
        # forceAspect(plt.gca(), 0.7)
        plt.gca().legend(legend_handle, legend_title, loc=loc, fontsize=30, labelspacing=0.1)
        plt.tick_params(axis='both', labelsize=30, pad=20)

        if (fplot != plt.loglog) and (fplot != plt.semilogy):
            plt.locator_params(axis='y', nbins=4)

        if (fplot != plt.loglog) and (fplot != plt.semilogx):
            plt.locator_params(axis='x', nbins=4)

        plt.tight_layout()
        plt.autoscale(enable=True, axis='x', tight=True)
        plt.savefig("../images/{}/{}{}.pdf".format(name,feature,n), bbox_inches='tight')

def make_feature_comp_tables(files, features, name, horizontal_splits=1, titles=None,
                             head_fmt=r":raw:`\multicolumn{{1}}{{c}}{{{}}}`",
                             data_fmt="{0:0.2f}", complexity_weight=0.02, rank=False,
                             rank_avg=[],
                             scale_acc=True
                             ):
    data, cvs = load_data(files, complexity_weight)
    if titles:
        for i, n in enumerate(titles):
            cvs[i]['desc'] = n

    for feature in features:
        if not rank:
            table = form_mean_table(data[feature])
            if feature == 'acc' and scale_acc:
                for ds in table:
                    for a in table[ds]:
                        table[ds][a] = tuple(v*100 for v in table[ds][a])
        else:
            table = anova(data[feature], feature_properties[feature]['desc'])
            mean_rank = form_mean_rank(table)

        csv_table = prepare_csv_table(table=table, cvs=cvs,
                                      head_fmt=head_fmt, data_fmt=data_fmt,
                                      sort_by_desc=False)

        if rank and rank_avg:
            csv_table.append(rank_avg + ['{:0.2f}'.format(mean_rank[c]) for c in cvs])

        write_csv_table("{}-{}.csv".format(name, feature), csv_table,
                        horizontal_splits=horizontal_splits)

def table_fig_dual_feature(files, features, name, rst_file, xvals, fignum=10, fig_plotsnum=5,
                           figs=None,cluster_by=None, plot_funcs=(plt.plot, plt.plot),
                           aspect=1, subfig_caption = "DT {feature}: {datasets}",
                           fig_caption = ("{name}", "{name}"), titles=None, locs=["lower left", "lower left"],
                           scale_acc = True
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
        if feature == 'acc' and scale_acc:
            for ds in table:
                for a in table[ds]:
                    table[ds][a] = tuple(v*100 for v in table[ds][a])

        plots = form_cluster_matrix(table)
        if feature == cluster_by:
            figs = form_clusters(plots,fignum,fig_plotsnum)

        print_figures(table,feature, plot, xvals=xvals, name=name, loc=l, figs=figs, aspect=aspect)
        dump_table_csv("{}-{}.csv".format(name, feature),
                       table, cvs, variance=False, sort_by_desc=False)

    subfigs = []
    for i,f in enumerate(figs):
        for j, feature in enumerate(features):
            if isinstance(f[0],str):
                datasets = ', '.join(f)
            else:
                datasets = ', '.join([list(sorted(table))[p] for p in f])

            subfigs.append(subfig_tmpl.format(name=name,
                                              feature=feature,
                                              id=i,
                                              caption=subfig_caption[j].format(feature=feature,
                                                                            datasets=datasets)
            ))

    for i in range(2):
        figure = fig_tmpl.format(name=name + str(i+1),
                                 subfigures=''.join(subfigs[i*10:(i+1)*10]),
                                 caption=fig_caption[i].format(name=name))
        substitute_subfigure(rst_file, figure, name + str(i+1))
