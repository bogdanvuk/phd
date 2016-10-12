from bdp import *
from dtdtools import draw_dt, balance_dt, templdef
from buchheim import buchheim

dt = {
    "0": {"lvl": 0, "id": 0,"cls": 0,"left": "1","right": "2","thr": -0.07812,"coeffs": [0.24533,-0.36081]},
    "1": {"lvl": 1, "id": 1,"cls": 0,"left": "3","right": "4","thr": 0.00000,"coeffs": []},
    "2": {"lvl": 1, "id": 2,"cls": 3,"left": "-1","right": "-1","thr": 0.00000,"coeffs": []},
    "3": {"lvl": 1, "id": 3,"cls": 1,"left": "-1","right": "-1","thr": 0.00000,"coeffs": []},
    "4": {"lvl": 1, "id": 4,"cls": 2,"left": "-1","right": "-1","thr": 0.00000,"coeffs": []}
    }

def conv2dttree(node, dt):
    node['c'] = []
    node['id'] += 1
    if node['left'] != '-1':
        node['c'] += [dt[node['left']], dt[node['right']]]

        for c in node['c']:
            conv2dttree(c, dt)

    return node

templdef['node'].nodesep = p(0.5, 1.5)
templdef['leaf'].nodesep = p(0.5, 1.5)
templdef['leaf'].size = p(3.2,1.8)

dt = conv2dttree(dt['0'], dt)
buchheim(dt)
root = draw_dt(dt)
bb = root._bounding_box()
canvas_size = p(12,9)
fig << '\definecolor{emphcolor}{RGB}{135,206,235}\n'
fig << '\definecolor{addcolor}{RGB}{235,206,135}\n'
fig << block(border=False, p=p(midx(bb[0], bb[1])-canvas_size[0]/2, 0), size=canvas_size)
root['left'].fill = 'emphcolor'
root['left']['left'].fill = 'addcolor'
root['left']['right'].fill = 'addcolor'
fig << root
