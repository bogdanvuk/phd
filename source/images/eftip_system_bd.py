from bdp import *

part = block(text_margin=p(0.5, 0.5), alignment="nw", dotted=True, group='tight', group_margin=[p(1,3), p(1,2)])

comp = block(size=p(6,4), nodesep=(2,2))
ps_comp = block(size=p(6,6), nodesep=(2,3))
bus_cap = cap(length=0.8, width=1.3, inset=0, type='Stealth')
bus_cap_small = bus_cap(length=0.4, width=0.6)
bus = path(style=(bus_cap, bus_cap), line_width=0.7, double=True, border_width=0.1)
bus_small = bus(style=(bus_cap_small, bus_cap_small), line_width=0.3, border_width=0.06)
bus_text = text(font="\\scriptsize", margin=p(0,0.5))
mem_bus_text = bus_text(margin=p(0,0.2))

#------------------------------------------------------------------------------ 
#  PS Block
#------------------------------------------------------------------------------ 

ps = part("Processing System")
ps['cpu'] = ps_comp("CPU")
ps['mem_con'] = ps_comp("DDR3 Memory Controller").below(ps['cpu'])

ddr3 = ps_comp("DDR3 Memory").left(ps['mem_con'])
fig << ddr3
fig << bus(ddr3.e(0.5), ps['mem_con'].w(0.5))
ps['intercon'] = block(r"AXI4 \\ Interconnect", ps['mem_con'].s(1.0)-ps['cpu'].n()).right(ps['cpu'])
ps['cpu2intercon'] = bus(ps['cpu'].e(2), ps['intercon'].w(2))
fig << bus_text("AXI4").align(ps['cpu2intercon'].pos(0.5), prev().s(0.5, 0.2))

ps['mem_con2intercon'] = bus(ps['mem_con'].e(0.5), p(ps['intercon'].w()[0], ps['mem_con'].e(0.5)[1]))
fig << bus_text("AXI4").align(ps['mem_con2intercon'].pos(0.5), prev().s(0.5, 0.2))

fig << ps

#------------------------------------------------------------------------------ 
# DTEEP Ensemble
#------------------------------------------------------------------------------ 

eftip = part("EFTIP co-processor", group_margin=[p(1,2), p(1,2)])

eftip['cu'] = comp("Control Unit", size=p(7,4), nodesep=(2,2)).right(ps['intercon'], 5).aligny(ps['cpu'].p)

eftip['inst_mem'] = comp("Training Set Memory").right(eftip['cu'])
eftip += bus_small(eftip['cu'].e(1), eftip['inst_mem'].w(1))

eftip['calc'] = comp("Accuracy Calculator").right(eftip['inst_mem'])
eftip += bus_small(eftip['calc'].n(0.5), eftip['calc'].n(0.5) - (0,1), eftip['cu'].n(0.5), 
                   style=('',bus_cap_small), routedef='-|')

array_part = block(text_margin=p(-0.5, 0.5), alignment="bc", dotted=True, group='tight', group_margin=[p(1,1), p(1,1)], text_font='\\footnotesize')

t_nte = block(size=(5, 6), nodesep=(4,1)) #, text_font='footnotesize')
t_dt_mem = t_nte(alignment="cw", text_margin=p(0.3, 0))
t_dt_submem = block(size=t_nte.size/2, dotted=True)

dt_mem = t_dt_mem()
dt_mem += t_dt_submem("CM").align(dt_mem.e(0), prev().e(0))
dt_mem += t_dt_submem("SM").align(dt_mem.e(1.0), prev().e(1.0))

dt_mem_array = array_part("DT Memory Array")

#Hack for bad group bdp design
dt_mem_array.group_margin[0] += p(2.5,0)
dt_mem_array += dt_mem("$L_1$").below(eftip['cu']).alignx(eftip['cu'].s(3))
dt_mem_array += dt_mem("$L_2$").below(dt_mem_array[-1])
dt_mem_array += dt_mem("$L_{D^M}$").below(dt_mem_array[-1], 3)

nte_array = array_part("Classifier")
cu2dtmem = net()
for name, d in zip(["$NTE_1$", "$NTE_2$", "$NTE_{D^M}$"], dt_mem_array):
    nte_array += t_nte(name).right(dt_mem_array[d])
    cu2dtmem += bus_small(eftip['cu'].s(1), dt_mem_array[d].w(0.5), routedef='|-')
    for i in range(2):
        for (j, name, style) in zip(range(2), ['addr', 'data'], [(bus_cap_small, ''), ('',bus_cap_small)]):
            pos = i*3 + j + 1
            eftip += bus_small(dt_mem_array[d].e(pos), nte_array[-1].w(pos), style=style)
            eftip += mem_bus_text(name).align(eftip[-1].pos(0.5), prev().s(0.5))

eftip += text(r"$\cdot\cdot\cdot$", font='\\footnotesize').align(mid(dt_mem_array[1].c(), dt_mem_array[2].c()), prev().c())

eftip += bus_small(nte_array[1].s(0.5), poffy(1), style=('',bus_cap_small))
eftip += text(r"$\cdot\cdot\cdot$", font='\\footnotesize').align(mid(nte_array[1].c(), nte_array[2].c()), prev().c())
eftip += bus_small(nte_array[0].s(0.5), nte_array[1].n(0.5), style=('',bus_cap_small))
eftip += bus_small(nte_array[2].n(0.5) - p(0, 1), poffy(1), style=('',bus_cap_small))

eftip += bus_small(nte_array[-1].e(0.5), eftip['calc'].s(0.5), style=('',bus_cap_small), routedef='-|')
eftip += nte_array
eftip += cu2dtmem
eftip += dt_mem_array

fig << eftip
fig << bus(p(ps['intercon'].e(3), eftip['cu'].w(3)), eftip['cu'].w(3), style=(bus_cap, bus_cap))
fig << bus_text("AXI4").alignx(mid(ps.e(), eftip.w()) + p(0.3,0), prev().c()).aligny(fig[-1].pos(0.5), prev().s(0, 0.2))
fig << path(eftip['cu'].w(1), ps['intercon'].e() + p(1.7,-1), ps['cpu'].n(0.5), routedef='-|', style=('', '>'))
fig << bus_text("IRQ").alignx(mid(ps.e(), eftip.w()) + p(0.3,0), prev().c()).aligny(eftip['cu'].w(1),prev().s(0, -0.1))

render_fig(fig)
