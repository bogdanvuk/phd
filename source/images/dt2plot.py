# dt = { '00': {'cls':0,
#               'id': 0,
#               'lvl': 0,
#               'coeffs': [0.2, 0.3],
#               'thr': 0.25,
#               'left': '10',
#               'right': '11'},
#        '10': {'cls':1,
#               'id': 0,
#               'lvl': 1,
#               'coeffs': [],
#               'thr': 0,
#               'left': '',
#               'right': ''},
#        '11': {'cls':0,
#               'id': 1,
#               'lvl': 1,
#               'coeffs': [0.2, -0.3],
#               'thr': -0.07,
#               'left': '21',
#               'right': '20'},
#        '20': {'cls':2,
#               'id': 0,
#               'lvl': 2,
#               'coeffs': [],
#               'thr': 0,
#               'left': '',
#               'right': ''},
#        '21': {'cls':0,
#               'id': 1,
#               'lvl': 2,
#               'coeffs': [1, 0],
#               'thr': 0.8,
#               'left': '30',
#               'right': '31'},
#        '30': {'cls':3,
#               'id': 0,
#               'lvl': 3,
#               'coeffs': [],
#               'thr': 0,
#               'left': '',
#               'right': ''},
#        '31': {'cls':4,
#               'id': 1,
#               'lvl': 3,
#               'coeffs': [],
#               'thr': 0,
#               'left': '',
#               'right': ''}
#
#
# }

#dt = {"(0,0)": {"lvl": 0, "id": 0,"cls": 0,"left": "(1,0)","right": "(1,1)","thr": -0.01953,"coeffs": [0.31268,-0.35934]},"(1,0)": {"lvl": 1, "id": 0,"cls": 0,"left": "(2,1)","right": "(2,2)","thr": 0.30469,"coeffs": [0.44415,0.11185]},"(2,1)": {"lvl": 2, "id": 1,"cls": 1,"left": "","right": "","thr": 0.00000,"coeffs": []},"(2,2)": {"lvl": 2, "id": 2,"cls": 2,"left": "","right": "","thr": 0.00000,"coeffs": []},"(1,1)": {"lvl": 1, "id": 1,"cls": 0,"left": "(2,2)","right": "(2,3)","thr": -0.16406,"coeffs": [-0.08939,-0.25507]},"(2,2)": {"lvl": 2, "id": 2,"cls": 2,"left": "","right": "","thr": 0.00000,"coeffs": []},"(2,3)": {"lvl": 2, "id": 3,"cls": 3,"left": "","right": "","thr": 0.00000,"coeffs": []}}


import matplotlib.pyplot as plt
import matplotlib
import attrspace_plot
import numpy as np
import math
import json
import dt2dot
from bdp import *
from dtdtools import draw_dt, balance_dt, templdef
from buchheim import buchheim

matplotlib.rcParams['contour.negative_linestyle'] = 'solid'

def lines_intersection(l1, l2):
    res = np.cross(l1, l2)
    if res[2] == 0:
        return None
    else:
        return np.array([res[0]/res[2], res[1]/res[2]])

axis_coefs = [
    np.array([1, 0, 0]),
    np.array([0, 1, 0]),
    np.array([1, 0, -1]),
    np.array([0, 1, -1])
]

axis_nodes = [
    np.array([0, 0]),
    np.array([0, 1]),
    np.array([1, 0]),
    np.array([1, 1])
]

def trim_outside_intersections(hier, path, intersections):
    rem = []
    for i, inter in enumerate(intersections):
        remove = False
        for a in [0,1]:
            if (inter[a] < 0) or (inter[a] > 1):
                remove = True
                break

        if not remove:
            for h,p in zip(hier, path):
                #print('h{}{}, p={} '.format(h['lvl'], h['id'], p))
                #print(inter, np.dot(inter, h['coeffs']) - h['thr'])
                if np.absolute(np.dot(inter, h['coeffs']) - h['thr']) < 1e-5:
                    continue
                elif ((np.dot(inter, h['coeffs']) < h['thr']) and (p == 'right')) or \
                     ((np.dot(inter, h['coeffs']) > h['thr']) and (p == 'left')):
                    remove = True
                    #print('Removed')
                    break

        if remove:
            rem.append(i)

    for i in reversed(rem):
        del intersections[i]


def get_intersections(hier, path, node):
    hcoef = node['coeffs'] + [-node['thr']]
    intersections = []
    for a in axis_coefs:
        inter = lines_intersection(hcoef, a)
        if inter is not None:
            intersections.append(inter)

    for h in hier:
        phcoef = h['coeffs'] + [-h['thr']]
        inter = lines_intersection(hcoef, phcoef)
        if inter is not None:
            intersections.append(inter)

    #print('{}{}: '.format(node['lvl'], node['id']))

    trim_outside_intersections(hier, path, intersections)

    #print(intersections)
    return intersections

def plot_subspace(dt, n, hier=[], path=[], alpha=1,
                  region_ttl = lambda i,c: '{}-$C_{}$'.format(i + 1, c)):
    if n['left'] != "-1":
        inter = get_intersections(hier, path, n)
        n['line'] = inter
        if hier is None:
            y,x=np.ogrid[0:1:100j,0:1:100j]
            plt.contour(x.ravel(), y.ravel(), n['coeffs'][0]*x + n['coeffs'][1]*y, [n['thr']], linewidths=2, colors='k', alpha=alpha)
        elif inter:
            #print(inter)
            plt.plot([inter[0][0], inter[1][0]], [inter[0][1], inter[1][1]], linewidth=2, linestyle='--', color='k', alpha=alpha)

        hier.append(n)
        for ch in ['left', 'right']:
            path.append(ch)
            plot_subspace(dt, dt[n[ch]], hier, path, alpha=alpha, region_ttl=region_ttl)
            path.pop()

        hier.pop()
    else:
        intersections = []
        intersections.extend(axis_nodes)
        for h in hier:
            intersections.extend(h['line'])

        trim_outside_intersections(hier, path, intersections)
        #print('CLASS: {}{}: '.format(n['lvl'], n['id']))
        #print(intersections)

        if intersections:
            import jarvis
            intersections = jarvis.convex_hull([i.tolist() for i in intersections])
            import centroids

            center = centroids.calculate_polygon_centroid(intersections + [intersections[0]])

#         center = np.array([0,0])
#         for inter in intersections:
#             center = np.add(center, inter)
#
#         center = 1/len(intersections)*center

            plt.text(center[0]-0.05, center[1], region_ttl(n['id'], n['cls']), size=25)
            #print('CLASS: {}{}: '.format(n['lvl'], n['id']))
            #print(intersections)

#print(get_intersections([], dt['00']))

def plot(dt, dataset, alpha=0.5,
         region_ttl = lambda i,c: '{}-$C_{}$'.format(i + 1, c)):
    plt.figure(0)
    attr, cls = attrspace_plot.load_arff(dataset)
    ds = {'attr': attr, 'cls': cls}
    attrspace_plot.plot(ds, (0,1), alpha=alpha)

    plot_subspace(dt, dt['0'], alpha=0.7, region_ttl=region_ttl)
    plt.gca().axes.get_xaxis().set_visible(False)
    plt.gca().axes.get_yaxis().set_visible(False)

    return plt

def plot2pdf(dt, pdffn, dataset, alpha=0.5):
    plot(dt, dataset, alpha=alpha)
    plt.savefig(pdffn, bbox_inches='tight')
    plt.close()

def conv2dttree(node, dt):
    node['c'] = []
    node['id'] += 1
    if node['left'] != '-1':
        node['c'] += [dt[node['left']], dt[node['right']]]

        for c in node['c']:
            conv2dttree(c, dt)

    return node

def plot_dts_iter():

    import os

    dataset = "../data/vene.csv"
    json_dir = '/data/projects/phd/source/images/efti_overview_dts/json'
    pdf_dir = '/data/projects/phd/source/images/efti_overview_dts'
    _, _, filenames = next(os.walk(json_dir), (None, None, []))
    efti_iters = sorted([int(os.path.splitext(f)[0]) for f in filenames])
    while len(efti_iters) > 8:
        min_rel_dist = max(efti_iters)
        rem_suggest = 0
        for i in range(1, len(efti_iters) - 1):
            rel_dist = (efti_iters[i+1] - efti_iters[i])/math.log(efti_iters[i])
            if rel_dist < min_rel_dist:
                min_rel_dist = rel_dist
                rem_suggest = i+1

        del efti_iters[rem_suggest]

    print(efti_iters)
    templdef['node'].nodesep = p(0.5, 1.5)
    templdef['leaf'].nodesep = p(0.5, 1.5)
    templdef['leaf'].size = p(3.2,1.8)
    for i, ei in enumerate(efti_iters):
        jsfn = os.path.join(json_dir, '{}.js'.format(ei))
        pdffn = os.path.join(pdf_dir, 'dt{0:02d}.pdf'.format(i))
        dotfn = os.path.join(pdf_dir, 'dt{0:02d}.dot'.format(i))
        dotpdffn = os.path.join(pdf_dir, 'dot{0:02d}.png'.format(i))

        with open(jsfn) as data_file:
            dt = json.load(data_file)

        plot2pdf(dt, pdffn, dataset, alpha=0.15)

        dt = conv2dttree(dt['0'], dt)
        buchheim(dt)
        root = draw_dt(dt)
        fig << root
        render_fig(fig, dotpdffn, options={'p': True, 'c': True} )
        fig.clear()

        # s = dt2dot.dt2dot(dt)

        # with open(dotfn, 'w') as fout:
        #     fout.write(s)

        # from subprocess import call
        # call(["dot", "-Tpng", dotfn, "-o", dotpdffn])

if __name__ == "__main__":
    plot_dts_iter()
# with open('/data/projects/phd/source/images/efti_overview_dts/json/177050.js') as data_file:
#     dt = json.load(data_file)

# dt = conv2dttree(dt['0'], dt)
# buchheim(dt)
# root = draw_dt(dt)
# fig << root
# render_fig(fig)
# print(dt)

# dt = {
#     "0": {"lvl": 0, "id": 0,"cls": 0,"left": "1","right": "2","thr": 1,"coeffs": [2,0]},
#     "1": {"lvl": 1, "id": 1,"cls": 0,"left": "3","right": "4","thr": -1,"coeffs": [6, 5]},
#     "2": {"lvl": 1, "id": 2,"cls": 0,"left": "5","right": "6","thr": -2,"coeffs": [6, 5]},
#     "3": {"lvl": 2, "id": 3,"cls": 1,"left": "-1","right": "-1","thr": 0.00000,"coeffs": []},
#     "4": {"lvl": 2, "id": 4,"cls": 2,"left": "-1","right": "-1","thr": 0.00000,"coeffs": []},
#     "5": {"lvl": 2, "id": 5,"cls": 1,"left": "-1","right": "-1","thr": 0.00000,"coeffs": []},
#     "6": {"lvl": 2, "id": 6,"cls": 3,"left": "-1","right": "-1","thr": 0.00000,"coeffs": []}
# }

# dt = {
#     "0": {"lvl": 0, "id": 0,"cls": 0,"left": "1","right": "2","thr": 1,"coeffs": [2,0]},
#     "1": {"lvl": 1, "id": 1,"cls": 0,"left": "3","right": "4","thr": -3,"coeffs": [8,-10]},
#     "2": {"lvl": 1, "id": 2,"cls": 0,"left": "5","right": "6","thr": 1,"coeffs": [8,-10]},
#     "3": {"lvl": 2, "id": 3,"cls": 1,"left": "-1","right": "-1","thr": 0.00000,"coeffs": []},
#     "4": {"lvl": 2, "id": 4,"cls": 0,"left": "7","right": "8","thr": 7,"coeffs": [8,10]},
#     "5": {"lvl": 2, "id": 5,"cls": 0,"left": "9","right": "10","thr": 11,"coeffs": [8,10]},
#     "6": {"lvl": 2, "id": 6,"cls": 2,"left": "-1","right": "-1","thr": 0.00000,"coeffs": []},
#     "7": {"lvl": 3, "id": 7,"cls": 1,"left": "-1","right": "-1","thr": 0.00000,"coeffs": []},
#     "8": {"lvl": 3, "id": 8,"cls": 2,"left": "-1","right": "-1","thr": 0.00000,"coeffs": []},
#     "9": {"lvl": 3, "id": 9,"cls": 1,"left": "-1","right": "-1","thr": 0.00000,"coeffs": []},
#     "10": {"lvl": 3, "id": 10,"cls": 2,"left": "-1","right": "-1","thr": 0.00000,"coeffs": []}
# }

# plot(dt, "dt_oblique_traversal.pdf", "../data/yingyang.csv")

# for name, n in dt.items():
#     if n['coeffs']:
#         plt.contour(x.ravel(), y.ravel(), n['coeffs'][0]*x + n['coeffs'][1]*y, [n['thr']], linewidths=2, colors='k')
