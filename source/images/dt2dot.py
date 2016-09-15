# dt = { '00': {'class':0,
#               'id': 0,
#               'level': 0,
#               'coef': [0.2, 0.3],
#               'thr': -0.17,
#               'left': '10',
#               'right': '11'},
#        '10': {'class':1,
#               'id': 0,
#               'level': 1,
#               'coef': [],
#               'thr': 0,
#               'left': '',
#               'right': ''},
#        '11': {'class':0,
#               'id': 1,
#               'level': 1,
#               'coef': [0.2, -0.3],
#               'thr': 0.17,
#               'left': '20',
#               'right': '21'},
#        '20': {'class':2,
#               'id': 0,
#               'level': 1,
#               'coef': [],
#               'thr': 0,
#               'left': '',
#               'right': ''},
#        '21': {'class':3,
#               'id': 1,
#               'level': 1,
#               'coef': [],
#               'thr': 0,
#               'left': '',
#               'right': ''}
# 
# }

#dt = {"(0,0)": {"lvl": 0, "id": 0,"cls": 0,"left": "(1,0)","right": "(1,1)","thr": -0.01953,"coeffs": [0.31268,-0.35934]},"(1,0)": {"lvl": 1, "id": 0,"cls": 0,"left": "(2,1)","right": "(2,2)","thr": 0.30469,"coeffs": [0.44415,0.11185]},"(2,1)": {"lvl": 2, "id": 1,"cls": 1,"left": "","right": "","thr": 0.00000,"coeffs": []},"(2,2)": {"lvl": 2, "id": 2,"cls": 2,"left": "","right": "","thr": 0.00000,"coeffs": []},"(1,1)": {"lvl": 1, "id": 1,"cls": 0,"left": "(2,2)","right": "(2,3)","thr": -0.16406,"coeffs": [-0.08939,-0.25507]},"(2,2)": {"lvl": 2, "id": 2,"cls": 2,"left": "","right": "","thr": 0.00000,"coeffs": []},"(2,3)": {"lvl": 2, "id": 3,"cls": 3,"left": "","right": "","thr": 0.00000,"coeffs": []}}

dot_tmplt = """
digraph foo {{
    edge [dir=none]
    node [fontsize=30]
    nodesep=0.5
    ranksep = "0.5 equally"
    {}
    {}
}}
"""

node_tmplt = '{} [shape={}]'
hier_tmplt = '{} -> {}'

class NodePool(list):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cnt = 0

    def insert(self, name, node):
        self.cnt += 1
        self.append(node)
        node['id'] = self.cnt
        node['name'] = name
        return node

def dt2dot(dt):
    node_pool = NodePool()
    node_pool.insert('0', dt['0'])

    hier = []
    node_def = []

    while node_pool:
        node = node_pool.pop(0)
        if node['left'] != "-1":
            node_def.append(node_tmplt.format(node['id'], 'circle'))
            for ch in ['left', 'right']:
                child = node_pool.insert(node[ch], dt[node[ch]])
                hier.append(hier_tmplt.format(node['id'], child['id']))
        else:
            node_def.append(node_tmplt.format(node['id'], 'square'))

    return dot_tmplt.format('\n    '.join(node_def), '\n    '.join(hier))


import json
with open('/data/personal/doktorat/prj/efti_pc/dt.js') as data_file:    
    dt = json.load(data_file)
    
s = dt2dot(dt)

with open('proba.dot', 'w') as fout:
    fout.write(s)
    
from subprocess import call
call(["dot", "-Tpng", "proba.dot", "-o", "proba.png"])
