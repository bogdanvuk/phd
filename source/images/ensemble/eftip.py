from bdp import *

comp = block(size=p(6,4), nodesep=(1,1))
bus_cap = cap(length=0.8, width=1.3, inset=0, type='Stealth')
bus = path(style=(bus_cap, bus_cap), line_width=0.7, double=True, border_width=0.1, shorten = [0.2, 0.2])
bus_text = text(font="\\scriptsize", margin=p(0,0.5))

pl = block("SMAE block", text_margin=p(0.5, 0.5), alignment="nw", dotted=True, group='tight', group_margin=[p(1,1.5), p(1,1)])
pl += comp("Control Unit")
fig << path(pl['Co'].w(1), poffx(-5), style=(None, '>'))
fig << text("IRQ").align(fig[-1].pos(0.5), prev().s(0.5, 0))
fig << bus(pl['Co'].w(3), poffx(-5))
fig << text("AXI4").align(fig[-1].pos(0.5), prev().s(0.5, 0.3))
pl += comp("Training Set Memory").below(pl['Co'], 3)
pl += bus(pl['Co'].s(0.5), pl['Tr'].n(0.5))

t_nte = block(size=(4, 2), nodesep=(3,1), font='\\footnotesize')


# dt_mem = block("DT Memory Array", text_margin=p(0, 1), alignment="bc", dotted=True, group='tight', text_font='\\footnotesize', group_margin=[p(1,1), p(1,1)])
dt_mem = block(dotted=True, group='tight', group_margin=[p(1,1), p(1,1)])

dt_mem += t_nte("$DTD_1$").right(pl['Co'], 3).aligny(pl['Co'].e(3))
dt_mem += t_nte("$DTD_2$").right(dt_mem['$DTD_1'])
dt_mem += t_nte("$DTD_{L_{m}}$").right(dt_mem['$DTD_2'], 2)

pl += text(r"$\cdot\cdot\cdot$", font='\\footnotesize').align(mid(dt_mem['$DTD_2'].c(), dt_mem['$DTD_{L_{m}}'].c()), prev().c())
pl += text("DT Memory Array", font='\\footnotesize').align(mid(dt_mem['$DTD_2'].c(), dt_mem['$DTD_{L_{m}}'].c()), prev().n(0.5, -0.7))

pl['dt_mem'] = dt_mem

dt_mem_net = net()

for d in dt_mem:
    dt_mem_net += bus(pl['Co'].e(1), dt_mem[d].n(0.5), routedef='-|')
    
pl += dt_mem_net
 
nte = block(dotted=True, group='tight', group_margin=[p(1,1), p(1,1)])
nte += t_nte("$TLE_1$").below(dt_mem[0]).aligny(pl['Tr'].e(0.5), prev().w(0.5))
nte += t_nte("$TLE_2$").below(dt_mem[1]).aligny(nte[-1].p)
pl += bus(nte[0].e(0.5), nte[1].w(0.5), style=('', bus_cap))
nte += t_nte("$TLE_{L_{m}}$").below(dt_mem[2]).aligny(nte[-1].p)
pl += bus(nte[1].e(0.5), nte[1].e(0.5) + (2,0), style=('', bus_cap))
pl += bus(nte[2].w(0.5), nte[2].w(0.5) - (2,0), style=(bus_cap, ''))
pl += text('$\cdot\cdot\cdot$').align(mid(nte[1].c(), nte[2].c()), prev().c())
pl += text("Classifier", font='\\footnotesize').align(mid(nte[1].c(), nte[2].c()), prev().n(0.5, -0.7))
pl += nte

pl += comp("Accuracy Calculator").aligny(pl['Co'].n(0, -0.2), prev().s()).alignx(dt_mem['*DTD_1'].c(), prev().w())
pl += bus(pl['Co'].n(0.5), pl['Ac'].w(0.5), routedef='|-')
# pl += bus(pl['Ac'].n(0.5), pl['Ac'].n(0.5) - (0,1), pl['Co'].n(0.5), style=('', bus_cap), routedef='-|')


pl += bus(nte[2].e(0.5), poffx(2), pl['Ac'].e(0.5), style=('', bus_cap), routedef='|-')
 
for n, d in zip(nte, dt_mem):
    pl += bus(dt_mem[d].s(0.5), nte[n].n(0.5))
    
     
pl += bus(pl['Tr'].e(0.5), nte[0].w(0.5), style=('', bus_cap))

fig << pl
#render_fig(fig, './eftip.pdf')

