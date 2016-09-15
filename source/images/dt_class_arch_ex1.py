from eftirun_findt import dt
from dtdtools import draw_dt, templdef
from bdp import *

bus_cap = cap(length=0.4, width=0.6, inset=0, type='Stealth')
bus = path(style=(bus_cap, bus_cap), line_width=0.3, double=True, border_width=0.06)

root = draw_dt(dt)

inst_net = net()
inst_net += bus(root.n(0.5), poffy(-2), style=(bus_cap, ''))
inst_net += bus(root.n(0.5) - p(0,1), root['right'].n(0.5), routedef='-|', style=('', bus_cap))
inst_net += bus(root.n(0.5) - p(0,1), root['left'].n(0.5), routedef='-|', style=('', bus_cap))
inst_net += bus(root.n(0.5) - p(0,1), root['left']['left'].n(0.5), routedef='-|', style=('', bus_cap))

def set_leaf_transparency(dt, opacity=1):
    if not len(dt):
        dt.opacity = opacity
        dt.text_opacity = opacity
    else:
        for c in [dt['left'], dt['right']]:
            set_leaf_transparency(c, opacity)

set_leaf_transparency(root, 0.5)


fig << root
fig << inst_net
fig << text('Instance').alignx(root.c(), prev().s(0.5)).aligny(root.c() - p(0, 3), prev().s())
fig << block('Demultiplexer', size=p(18,2)).alignx(root.c(), prev().c()).aligny(root['left']['left']['left'].s() + p(0,1), prev().n())
fig << block('Class', opacity=0).below(fig['Demulti']).alignx(fig['Demulti'].c(), prev().c())
fig << bus(fig['Demulti'].s(0.5), fig['Class'].n(0.5), style=('', bus_cap))

demux_path = path(style=('', '>'), shorten=(0, 0.2))

fig << demux_path(root['left']['left']['aleft'][1] + p(0.8, -1), Precty(fig['Demulti'].n()))
fig << demux_path(root['left']['left']['aright'][1] + p(-0.8, -1), Precty(fig['Demulti'].n()))
fig << demux_path(root['left']['aright'][1] + p(-0.8, -1), Precty(fig['Demulti'].n()))
fig << demux_path(root['right']['aright'][1] + p(-0.8, -1), Precty(fig['Demulti'].n()))
fig << demux_path(root['right']['aleft'][1] + p(0.8, -1), Precty(fig['Demulti'].n()))
#print(root['left']['left']['aleft'][1])
#render_fig(fig)
