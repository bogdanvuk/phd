import matplotlib.pyplot as plt
import math
import numpy as np
import matplotlib

def plot_topomut(max_size,
                 c,
                 k = [0.1, 1, 2],
                 topo_mut = [0.1, 0.3, 0.6],
                 loc = "upper left",
                 aspect=0.6):

    x = np.array(list(range(max_size)))
    # y = [prob(i, 0.1, 5e-5, 0.05) for i in x]

    w, h = matplotlib.figure.figaspect(aspect)
    fig = plt.figure(figsize=(w,h))

    if len(k) > 1:
        legend_title = [r'$k_\rho = {}$'.format(kk) for kk in k]
    else:
        legend_title = [r'$\rho_0 = {}$'.format(t) for t in topo_mut]

    legend_handle = []
    for kk in k:
        for t in topo_mut:
            y = t*(1 - np.exp(-x/(kk*c)))
            line, = plt.plot(x,y, linewidth=4)
            legend_handle.append(line)

    plt.gca().legend(legend_handle, legend_title, loc=loc, fontsize=25, labelspacing=0.1)
    plt.tick_params(axis='both', labelsize=20, pad=10)
    plt.locator_params(axis='y', nbins=4)
    plt.locator_params(axis='x', nbins=4)
    plt.tight_layout()
    plt.autoscale(enable=True, axis='x', tight=True)
    # plt.gca().set_ylim([0,1])
    plt.ylabel(r'$\rho(N_l)$', size=30, rotation=0, labelpad=20)
    plt.xlabel(r'DT size: $N_l$', size=30)

    return plt

# plt = plot_topomut(180, 60, topo_mut=[0.6], loc="lower right")
# plt = plot_topomut(180, 60, k=[1], loc="upper left")
# plt.show()
