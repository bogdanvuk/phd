import os
import json
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.ticker import FuncFormatter

def load_js_data(fname):
    with open(fname) as data_file:
        res = json.load(data_file)

    return res

@FuncFormatter
def to_k(y, position):
    return r"{}k".format(int(y/1000))

def reposition_search_points(data):

    to_append = {}
    for i,d in enumerate(data):
        if d['name'] == 'SP':
            to_append[i] = {
                'name': 'SP',
                'iter':d['iter']-1,
                'size': data[i-1]['size'],
                'fit': data[i-1]['fit']
            }

            d['name'] = ''
        # elif d['name'] = 'RB':

    for a in sorted(to_append, reverse=True):
        data.insert(a, to_append[a])

    data.append({
                'name': '',
                'iter':1e6,
                'size': data[-1]['size'],
                'fit': data[-1]['fit']
            })

def plot_markers(data):
    for d in data:
        if d['name'] == 'SP':
            m = 'v'
            c = 'y'
        elif d['name'] == 'RB':
            m = 'D'
            c = 'r'
        else:
            m = None

        if m:
            plt.scatter([d['iter']], [d['fit']], marker=m, c=c, s=120, zorder=2)

def plot_fitpath(fn):
    data = load_js_data(fn)['event']
    reposition_search_points(data)

    x = []
    y = []
    for d in data:
        x.append(d['iter'])
        y.append(d['fit'])

    return plt.step(x, y, zorder=1, linewidth=3)

    # plot_markers(data)


def plot_fitpath_comp(fns, labels, aspect=1):
    w, h = matplotlib.figure.figaspect(aspect)
    fig = plt.figure(figsize=(w,h))

    legend_handle = []
    for fn in fns:
        line, = plot_fitpath(fn)
        legend_handle.append(line)

    plt.gca().legend(legend_handle, labels, loc='lower right')
    return plt
