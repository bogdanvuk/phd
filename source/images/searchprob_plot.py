import os
import math
import matplotlib.pyplot as plt
import matplotlib

def prob(i, dist, si, sp):
    return i * si * math.exp(-dist/sp)

def cumul(fprob, max_iter, dist, si, sp):
    q = 1
    total = 0
    for i in range(max_iter):
        p = prob(i, dist, si, sp)
        total += q*p
        q *= (1-p)
        yield total

def plot_searchprob(max_iter,
                    si,
                    sp,
                    dists = [0.4, 0.2, 0.1, 0.05, 0.01],
                    loc = "upper left",
                    aspect=0.6):

    x = list(range(max_iter))
    # y = [prob(i, 0.1, 5e-5, 0.05) for i in x]

    w, h = matplotlib.figure.figaspect(aspect)
    fig = plt.figure(figsize=(w,h))

    legend_title = [str(int(d*100)) + '%' for d in dists]
    legend_handle = []
    for d in dists:
        y = list(cumul(prob, max_iter, d, si, sp))
        line, = plt.plot(x,y, linewidth=4)
        legend_handle.append(line)

    plt.gca().legend(legend_handle, legend_title, loc=loc, fontsize=25, labelspacing=0.1)
    plt.tick_params(axis='both', labelsize=20, pad=10)
    plt.locator_params(axis='y', nbins=4)
    plt.locator_params(axis='x', nbins=4)
    plt.tight_layout()
    plt.gca().set_ylim([0,1])
    plt.ylabel('p', size=30, rotation=0, labelpad=20)
    plt.xlabel('iterations without advancement', size=30)

    return plt
