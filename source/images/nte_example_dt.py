from eftirun_findt import dt
from dtdtools import draw_dt, templdef, dt_for_hw
import copy
from bdp import *
from buchheim import buchheim
# from dt2dot import

bus_cap = cap(length=0.4, width=0.6, inset=0, type='Stealth')
bus = path(style=(bus_cap, bus_cap), line_width=0.3, double=True, border_width=0.06)
lvl_path = path(dotted=True)

templdef['node'].nodesep = (0.5, 2)
templdef['leaf'].nodesep = (0.8, 2)
# dt = conv2dttree(dt['0'], dt)
dt = copy.deepcopy(dt)
dt_for_hw(dt, 0)
buchheim(dt)
root = draw_dt(dt, templdef)
# dt = copy.deepcopy(dt)
# dt_for_hw(dt, 0)
# root = draw_dt(dt)
fig.package.add('amsmath')
fig << root

def coef2hex(val):
    return '{:04X}'.format(int(val) & (2**16-1))

def draw_coeffs(node, bdp_node, pos='right'):
    if node['c']:
        w = [coef2hex(w*32768) for w in node['w']]
        w.append(coef2hex(node['thr']*32768/(1 << 1)))
        t_float = r"""
$
\begin{{alignedat}}{{3}}
& \mathbf{{w}} = [{:.3f},\, &{:.3f}], \, &\theta={:.3f} \\
& \mathbf{{w}} = [\mathtt{{{}}},\, &\mathtt{{{}}}], \, &\theta=\mathtt{{{}}}
\end{{alignedat}}
$
        """.format(*(node['w'] + [node['thr']] + w))
        t_float = t_float.strip().replace('\n', '')
        # print(t_float)
        #print(t)
        fig << getattr(text(t_float, margin=p(-0.2,-1)), pos)(bdp_node)
        # fig << text(t_float, margin=p(0,0)).align(fig[-1].n(), cur().s())
        draw_coeffs(node['c'][0], bdp_node['left'], 'left')
        draw_coeffs(node['c'][1], bdp_node['right'], 'right')

draw_coeffs(dt, root)

# render_fig(fig)
