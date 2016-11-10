from bdp import *

bus_cap = cap(length=0.8, width=1.3, inset=0, type='Stealth')
bus_cap_small = bus_cap(length=0.4, width=0.6)
bus = path(style=(bus_cap, bus_cap), line_width=0.7, double=True, border_width=0.1)
bus_small = bus(style=(bus_cap_small, bus_cap_small), line_width=0.3, border_width=0.06)
bus_text = text(font="\\scriptsize", margin=p(0,0.5))

def make_nte(name, pos):
    nte = block(size=p(10,14), p=pos)
    pin_text = block(text_font='\\footnotesize', text_margin=p(0.2, 0), alignment='cw', border=False)
    fig << pin_text(r"Instance \\ Input").align(nte.w(2), prev().w(0.5))
    fig << pin_text(r"Node ID \\ Input").align(nte.w(5), prev().w(0.5))

    fig << pin_text(r"Instance \\ Output").align(nte.e(2), prev().e(0.5))
    fig << pin_text(r"Node ID \\ Output").align(nte.e(5), prev().e(0.5))

    fig << pin_text(r"CM addr").align(nte.w(8), prev().w(0.5))
    fig << pin_text(r"CM data").align(nte.w(9), prev().w(0.5))

    fig << pin_text(r"SM addr").align(nte.w(11), prev().w(0.5))
    fig << pin_text(r"SM data").align(nte.w(12), prev().w(0.5))

    fig << nte
    fig << text("NTE" + name).align(nte.n(0), prev().s(0))

    return nte

nte = []
nte.append(make_nte('$_{1}$', p(0, 0)))
nte.append(make_nte('$_{2}$', p(15, 0)))
nte.append(make_nte('$_{D^{M}}$', p(37, 0)))

# bus = path(double=True, thick=False)
# bus_text = text(font="tiny", margin=p(0,0))

fig << bus(nte[0].e(2), nte[1].w(2), style=('', bus_cap))
fig << bus(nte[0].e(5), nte[1].w(5), style=('', bus_cap))

fig << bus(nte[1].e(2), nte[1].e(2) + (3,0), style=('', bus_cap))
fig << bus(nte[1].e(5), nte[1].e(5) + (3,0), style=('', bus_cap))

fig << bus(nte[2].w(2) - (3,0), nte[2].w(2), style=('', bus_cap))
fig << bus(nte[2].w(5) - (3,0), nte[2].w(5), style=('', bus_cap))

fig << text("$\cdot\cdot\cdot$", font="\\Large").align(mid(nte[1].c(), nte[2].c()) - p(0,2), prev().c())

fig << bus(nte[0].w(2) - (6, 0), nte[0].w(2), style=('', bus_cap))
fig << bus(nte[0].w(5) - (2, 0), nte[0].w(5), style=('', bus_cap))
fig << text("0").align(fig[-1][0], prev().e(0.5))
#fig << path([nte[0].w(8) - (2, 0), nte[0].w(8), style='->')
# text("0").align(prev(1)[0], prev().e(0.5))()

for i in range(3):
    fig << bus_small(nte[i].w(8) + (-4, 9), nte[i].w(8), routedef='|-', style=('', bus_cap_small))
    fig << bus_small(nte[i].w(9) + (-3, 8), nte[i].w(9), routedef='|-', style=(bus_cap_small, ''))
    fig << bus_small(nte[i].w(11) + (-2, 6), nte[i].w(11), routedef='|-', style=('', bus_cap_small))
    fig << bus_small(nte[i].w(12) + (-1, 5), nte[i].w(12), routedef='|-', style=(bus_cap_small, ''))

fig << bus(nte[2].e(2), nte[2].e(2) + (3, 0), style=('', bus_cap))
fig << bus(nte[2].e(5), nte[2].e(5) + (3, 0), style=('', bus_cap))

fig << block("Classifier", nte[2].s(1.0) - nte[0].n() + (6.5,5), alignment="nw", text_font='\\Large', dotted=True, text_margin=(1, 0.8)).align(nte[0].n() - (5, 4), prev().n())

# render_fig(fig)
