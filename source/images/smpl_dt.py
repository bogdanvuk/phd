from eftirun_findt import dt
from dtdtools import draw_dt, templdef
from bdp import *

bus_cap = cap(length=0.4, width=0.6, inset=0, type='Stealth')
bus = path(style=(bus_cap, bus_cap), line_width=0.3, double=True, border_width=0.06)
lvl_path = path(dotted=True)

templdef['node'].nodesep = (0.3, 2)
root = draw_dt(dt)

startx = root['left']['left']['left'].n()[0] - 1
endx = root['right']['right'].n(1.0)[0] + 12

lvly = [
    mid(root.c(), root['left'].c())[1],
    mid(root['left'].c(), root['left']['left'].c())[1],
    mid(root['left']['left'].c(), root['left']['left']['left'].c())[1]
]

fig << lvl_path([startx, lvly[0]], poffx(endx-startx))
fig << text("Level 1").alignx(startx, cur().e(0.5)).aligny(root.w(0.5), cur().c())
fig << lvl_path([startx, lvly[1]], poffx(endx-startx))
fig << text("Level 2").alignx(startx, cur().e(0.5)).aligny(root['left'].w(0.5), cur().c())
fig << lvl_path([startx, lvly[2]], poffx(endx-startx))
fig << text("Level 3").alignx(startx, cur().e(0.5)).aligny(root['left']['left'].w(0.5), cur().c())

fig << block('$L_1$ Universal node').alignx(endx - 10, cur().n()).aligny(root.c(), cur().c())
fig << block('$L_2$ Universal node').alignx(fig['*L_1*'].p).aligny(root['left'].c(), cur().c())
fig << block('$L_3$ Universal node').alignx(fig['*L_1*'].p).aligny(root['left']['left'].c(), cur().c())

for i,y in enumerate(lvly):
    fig['reg{}'.format(i+1)] = block('reg').alignx(fig['*L_1*'].c(), cur().c()).aligny(y, cur().c())

for i in range(len(lvly)):
    #print(fig['L{}*'.format(i+1)].s(0.5))
    fig << bus(fig['*L_{}*'.format(i+1)].s(0.5), poffy(0.6), style=('', bus_cap))
    fig << bus(fig['reg{}'.format(i+1)].s(0.5), poffy(0.6), style=('', bus_cap))

fig << text('Class').below(fig['reg3'],1).alignx(fig['*L_1*'].c(), cur().c())

fig << root

for base in [fig['*L_1*'], root]:
    fig << text('Instance').aligny(base.c() - p(0,3),cur().c()).alignx(base.c(), cur().c())
    fig << bus(base.n(0.5), fig[-1].s(0.5), style=(bus_cap, ''), shorten=p(0.2, 0.1))

#render_fig(fig)
