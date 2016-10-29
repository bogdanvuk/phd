from bdp import *

pin_extrude = 2


mul_block = block("x", size=p(2,2), shape='circle')
add_block = block("+", size=p(2,2), shape='circle')
fifo_item = block(size=p(5,3), nodesep=p(0,0))
fifo_blk = block(text_margin=p(0.5, 0), alignment="tw", border=False, group='tight')

bus_cap = cap(length=0.4, width=0.6, inset=0, type='Stealth')
bus = path(color="black!40", style=('', bus_cap), shorten=p(0.2,0.2), line_width=0.3, border_width=0.06, double=True)
bus_text = text(font="\\footnotesize", margin=p(0.4,0.2))

nte = block("Node Test Evaluator - NTE", text_margin=p(0.5, 0.5), alignment="nw", dotted=True, group='tight', group_margin=[p(4,7), p(3,1)], text_font="\\Large")

def make_external(pos, direction='o'):
    if direction == 'o':
        style=('', bus_cap)
    else:
        style=(bus_cap, '')
    return bus(pos, poffx(nte.w() - pos - p(pin_extrude,0)), style=style)

#pin_leftx = evaluator.p[0] - 2

inst_fifo_text = [
    "$I_{i+N_P-1}$",
    "$I_{i+N_P-2}$",
    "$\cdot\cdot\cdot$",
    "$I_{i+1}$",
    "$I_{i}$",
]

inst_fifo = fifo_blk("Instance Queue")
for i,t in enumerate(inst_fifo_text):
    if i == 0:
        inst_fifo += fifo_item(t, size=p(11,3))
    else:
        inst_fifo += fifo_item(t).right(inst_fifo[-1])

nte += inst_fifo

inp_coef_tmpl = block(size=p(3,2), border=False, alignment="ce", nodesep=(1, 0.5), text_margin=p(0,0))

inp_coef_text = [
    "$w_{1}$",
    "$x_{1}$",
    "$w_{2}$",
    "$x_{2}$",
    "$w_{N^{M}_{A}-1}$",
    "$x_{N^{M}_{A}-1}$",
    "$w_{N^{M}_{A}}$",
    "$x_{N^{M}_{A}}$"
]

inp_coefs = group()
for i,t in enumerate(inp_coef_text):
    if i == 0:
        inp_coefs += inp_coef_tmpl(t).align(inst_fifo[0].s(1.0) + p(-5.5,1), cur().n(1.0))
    elif i == 4:
        inp_coefs += inp_coef_tmpl(t).below(inp_coefs[-1], 2)
    else:
        inp_coefs += inp_coef_tmpl(t).below(inp_coefs[-1])


nte += inp_coefs

w_net = net()
for i in range(len(inp_coefs)//2):
    w_net += bus(inst_fifo[0].s(1), inp_coefs[2*i+1].w(0.5), routedef='|-', shorten=p(0, 0.2))

nte += w_net

mul = group()
for i in range(len(inp_coefs)//2):
    mul += mul_block().aligny(mid(inp_coefs[2*i].p, inp_coefs[2*i+1].p)).alignx(inst_fifo[0].e() - p(2.5,0), cur().c())
    fig << path(inp_coefs[2*i].c(), mul[i].c(), shorten=(2, 1.5), style=('','>'), thick=True)
    fig << path(inp_coefs[2*i+1].c(), mul[i].c(), shorten=(2, 1.5), style=('','>'), thick=True)

nte += mul

fig << text(r"$\cdot$ \\ $\cdot$ \\ $\cdot$", font="\\normalsize").alignx(mul[1].c(), cur().c()).aligny(mid(mul[1].c(), mul[2].c()), cur().c())

add = group()

for i in range(len(mul)//2):
    add += add_block().aligny(mid(mul[2*i].p, mul[2*i+1].p)).alignx(inst_fifo[1].c(), cur().c())
    nte += block(size=p(0.5, 1.2)).align(mid(add[i].c(), mul[2*i].c()), prev().c())
    fig << path(mul[2*i].c(), add[i].c(), shorten=(1.2, 3.3), style=('','>'), thick=True)
    fig << path(mul[2*i].c(), add[i].c(), shorten=(3.3, 1.2), style=('','>'), thick=True)
    nte += block(size=p(0.5, 1.2)).align(mid(add[i].c(), mul[2*i+1].c()), prev().c())
    fig << path(mul[2*i+1].c(), add[i].c(), shorten=(1.2, 3.3), style=('','>'), thick=True)
    fig << path(mul[2*i+1].c(), add[i].c(), shorten=(3.3, 1.2), style=('','>'), thick=True)

add += add_block().aligny(mid(add[0].p, add[1].p)).alignx(inst_fifo[-2].c(), cur().c())

nte += add

for i in range(2):
    if i == 0:
        offset = (2.5, 1.2)
    else:
        offset = (2.5, -1.2)

    fig << path(add[i].c(), add[i].c() + offset, shorten=(1.2, 0.5), style=('','>'), thick=True)
    fig << path(add[-1].c() - offset, add[-1].c(), shorten=(0.5, 1.2), style=('','>'), thick=True)

    nte += block(size=p(0.5, 1.5)).align(add[i].c() + offset, prev().c())
    nte += block(size=p(0.5, 2)).align(add[-1].c() - offset, prev().c())

    nte += text("$\cdot\cdot\cdot$", font="\\large").align(mid(add[i].c(), add[2].c()), prev().c())

final_add_reg = block(size=p(0.5, 1.2)).align(add[2].c() + (2.5, 0), prev().c())
nte += final_add_reg
fig << path(add[-1].c(), final_add_reg.w(0.5), shorten=(1.1, 0.1), style=('','>'), thick=True)

struct_mem_reg = block(size=(0.5, 6)).below(inp_coefs[7], 0).alignx(inst_fifo[-2].e(0), prev().c())
nte += struct_mem_reg

node_fifo_text = [
    "$N_{i+N_P-1}$",
    "$N_{i+N_P-2}$",
    "$\cdot\cdot\cdot$",
    "$N_{i+1}$",
    "$N_{i}$",
]

node_fifo = fifo_blk("Node Queue")
for i,t in enumerate(node_fifo_text):
    if i == 0:
        node_fifo += fifo_item(t, size=p(11,3)).below(struct_mem_reg, 3).alignx(inst_fifo[0].p)
    else:
        node_fifo += fifo_item(t).right(node_fifo[-1])

nte += node_fifo

struct_mem_intf = block(r"Structural Memory Interface", size=p(6,6)).align(struct_mem_reg.c() - (4,0), prev().e(0.5))
nte += struct_mem_intf
fig << bus(node_fifo[-2].n(0.5), node_fifo[-2].n(0.5) - (0,1), struct_mem_intf.s(0.5), routedef='-|')
fig << bus_text("Node ID", margin=(1, 0.5)).align(fig[-1][2], prev().s())
fig << bus(struct_mem_intf.e(1), struct_mem_reg.w(1))
fig << bus_text(r"$\theta$").align(fig[-1][0], prev().s())
fig << bus(struct_mem_intf.e(3), struct_mem_reg.w(3))
fig << bus_text(r"$ChR$").align(fig[-1][0], prev().s())
fig << bus(struct_mem_intf.e(5), struct_mem_reg.w(5))
fig << bus_text(r"$ChL$").align(fig[-1][0], prev().s())

mem_intf = block(r"Coefficient Memory Interface", size=p(6,6)).align(mid(mul[0].c(), mul[-1].c()) - (11,0), prev().e(0.5))
nte += mem_intf

fig << make_external(inst_fifo[0].w(0.5), direction='i')
fig << bus_text(r"Instance \\ Input").aligny(fig[-1][-1], cur().s()).alignx(nte.w())

fig << make_external(struct_mem_intf.w(2))
fig << bus_text("SM addr").alignx(nte.w()).aligny(struct_mem_intf.w(2), prev().s())
fig << make_external(struct_mem_intf.w(4), direction='i')
fig << bus_text(r"SM data").alignx(nte.w()).aligny(struct_mem_intf.w(4), prev().s())

fig << make_external(mem_intf.w(2))
fig << bus_text(r"CM addr", margin=(0.3, 0.4)).alignx(nte.w()).aligny(mem_intf.w(2), cur().s())
fig << make_external(mem_intf.w(5), direction='i')
fig << bus_text(r"CM data", margin=(0.3, 0.4)).alignx(nte.w()).aligny(mem_intf.w(5), cur().s())

mem_intf_net = net()
coef_net = net()
for i in range(len(inp_coefs)//2):
    mem_intf_net += bus(mem_intf.e(3), mem_intf.e(3) + (1,0), p(inst_fifo[0].n()[0], inp_coefs[2*i].w(0.5)[1]), routedef='|-', shorten=p(0, 0.3))
    coef_net += bus(p(inst_fifo[0].n()[0], inp_coefs[2*i].w(0.5)[1]), inp_coefs[2*i].w(0.5), shorten=p(0.3, 0.3))
    nte += block(size=p(0.5, 1.2)).alignx(inst_fifo[0].n(), cur().c()).aligny(inp_coefs[2*i].w(0.5), cur().c())

fig << coef_net
fig << mem_intf_net

node_id_net = net()
node_id_net += make_external(node_fifo[0].w(0.5), direction='i')
fig << bus_text(r"Node ID Input").aligny(node_id_net[0][-1], prev().s()).alignx(nte.w())
node_id_net += bus(node_id_net[0][-1], mem_intf.s(4), routedef='-|')

fig << node_id_net

comp = block("$\leq$", p(3,3), text_font="\\large").right(add[-1], 4).aligny(add[-1].c(), prev().w(1))
nte += comp
fig << bus(final_add_reg.e(0.5), comp.w(1), shorten=p(0.3, 0.2))
fig << text("$\sum\limits_{i=1}^{N^{M}_{A}}w_{i}\cdot x_{i}$").align(comp.w(1) + (0.5,-1), prev().s(1.0))

mux_tmpl = block("MUX1", p(3,3), text_margin=p(0,1), alignment='nc')

mux = mux_tmpl().right(comp, 2)
nte += mux
fig << bus_text("0").align(mux.s(1), prev().s(0.5))
fig << bus_text("1").align(mux.s(2), prev().s(0.5))

fig << bus(struct_mem_reg.e(1), struct_mem_reg.e(1) + (1,0), comp.w(2), routedef='|-', shorten=p(0,0.2))
fig << bus(struct_mem_reg.e(3), mux.s(1), routedef='-|')
fig << bus(struct_mem_reg.e(5), mux.s(2), routedef='-|')

fig << path(comp.e(0.5), mux.w(0.5), style=('', '>'), shorten=p(0.1,0.1))

mux2 = mux_tmpl("MUX2").over(mux, 2).alignx(mux.e(), cur().s(1))
nte += mux2
fig << bus_text("0").align(mux2.s(1), prev().s(0.5))
fig << bus_text("1").align(mux2.s(2), prev().s(0.5))
fig << bus(mux.n(0.5), poffy(-1), mux2.s(1), routedef='-|')
fig << bus(node_fifo[-1].e(0.5), mux2.s(2), routedef='-|')
fig << bus_text(r"Node ID").align(fig[-1][0], prev().s())

fig << path((mux2.s(2)[0], node_fifo[-1].e(0.5)[1]), (mux2.e(0.5)[0] + 2, node_fifo[-1].e(0.5)[1]),mux2.e(0.5), routedef='|-', style=('','>'), shorten=p(0.2, 0.1))
fig << bus_text(r"[MSB]").alignx(mux2.s(2), prev().s()).aligny(node_fifo[-1].e(0.5), cur().s())

fig << bus(mux2.n(0.5), p(nte.e()[0] + 2, mux2.n()[1] -2), routedef='|-')
fig << bus_text("Node ID Output").aligny(fig[-1][1], cur().s()).alignx(nte.e(), cur().s(1.0))

fig << bus(inst_fifo[-1].e(0.5), p(nte.e()[0] + 2, inst_fifo[-1].c()[1]))
fig << bus_text("Instance Output").aligny(fig[-1][1], prev().s()).alignx(nte.e(), prev().s(1.0))

stages = [
    r'Stage \\ 1',
    r'Stage \\ 2',
    r'$\cdot\cdot\cdot$',
    r'Stage \\ $N_p - 1$',
    r'Stage \\ $N_p$'
]

for stage_id, (n, i, s) in enumerate(zip(node_fifo, inst_fifo, stages)):
    fig << path(inst_fifo[i].n() - p(0, 4), node_fifo[n].n(), dotted=True)
    if stage_id == len(inst_fifo) - 1:
        fig << block(s, border=False).aligny(inst_fifo[i].n() - p(0,2), cur().s()).alignx(mid(inst_fifo[i].n(), nte.e()), cur().c())
    else:
        fig << block(s, border=False).aligny(inst_fifo[i].n() - p(0,2), cur().s()).alignx(inst_fifo[i].c(), cur().c())

fig << path(inst_fifo[0].n() - p(0, 2), poffx(nte.e() - inst_fifo[0].n()), dotted=True)

fig << nte
# render_fig(fig)
