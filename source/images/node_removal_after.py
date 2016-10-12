from bdp import *
from dtdtools import draw_dt, balance_dt, templdef
from buchheim import buchheim

dt = {
    "0": {"lvl": 0, "id": 0,"cls": 0,"left": "1","right": "2","thr": -0.09375,"coeffs": [0.24350,-0.48581]},
    "1": {"lvl": 2, "id": 1,"cls": 0,"left": "3","right": "4","thr": 0.08398,"coeffs": [-0.02158,0.19016]},
    "3": {"lvl": 3, "id": 3,"cls": 3,"left": "-1","right": "-1","thr": 0.00000,"coeffs": []},
    "4": {"lvl": 3, "id": 4,"cls": 2,"left": "-1","right": "-1","thr": 0.00000,"coeffs": []},
    "2": {"lvl": 1, "id": 2,"cls": 0,"left": "5","right": "6","thr": 0.26953,"coeffs": [0.19818,0.32697]},
    "5": {"lvl": 2, "id": 5,"cls": 3,"left": "-1","right": "-1","thr": 0.00000,"coeffs": []},
    "6": {"lvl": 2, "id": 6,"cls": 2,"left": "-1","right": "-1","thr": 0.00000,"coeffs": []}
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
canvas_size = p(12,12.5)
fig << '\definecolor{emphcolor}{RGB}{135,206,235}\n'
fig << block(border=False, p=p(midx(bb[0], bb[1])-canvas_size[0]/2, 0), size=canvas_size)
root['left'].fill = 'emphcolor'
root['left']['left'].fill = 'emphcolor'
root['left']['right'].fill = 'emphcolor'
fig << root
