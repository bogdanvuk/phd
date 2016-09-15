from bdp import *

part = block(text_margin=p(0.5, 0.5), alignment="nw", dotted=True, group='tight', group_margin=[p(1,2), p(1,2)])

comp = block(size=p(6,4), nodesep=(2,2))
ps_comp = block(size=p(6,6), nodesep=(2,3))
bus_cap = cap(length=0.8, width=1.3, inset=0, type='Stealth')
bus = path(style=(bus_cap, bus_cap), line_width=0.7, double=True, border_width=0.1)
bus_text = text(font="\\scriptsize", margin=p(0,0.5))

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

eeftip = part("Ensemble DTEEP", group_margin=[p(0,2), p(1,2)])

eeftip['status'] = comp("IRQ Status", size=p(7,4), nodesep=(2,2)).right(ps['intercon'], 6).aligny(ps['cpu'].p)
eftip = block(size=p(6,3), nodesep=(1,1))
eeftip += eftip("$SMAE_1$").below(eeftip['status'], 1).movex(1)
eeftip += eftip("$SMAE_2$").below(eeftip["$S*1*"], 1)
eeftip += eftip("$SMAE_{S_m}$").below(eeftip["$S*2*"], 3)

eeftip_axi_enter = eeftip['status'].w(0.5) - (3,0)

eeftip += net(bus(eeftip_axi_enter, eeftip['status'].w(0.5), style=('=', bus_cap)),
              bus(eeftip_axi_enter + (1,0), eeftip['$S*1*'].w(0.5), routedef = '|-', style=('', bus_cap)),
              bus(eeftip_axi_enter + (1,0), eeftip['$S*2*'].w(0.5), routedef = '|-', style=('', bus_cap)),
              bus(eeftip_axi_enter + (1,0), eeftip['$S*{S_m}*'].w(0.5), routedef = '|-', style=('', bus_cap))
              )

bus_cap_small = bus_cap(length=0.4, width=0.6)
eeftip += bus(eeftip['status'].e(0.5), poffx(1), eeftip['$S*{S_m}*'].e(0.8) + (1,0), routedef='|-', line_width=0.3, style=(bus_cap_small, ''))
eeftip += path(eeftip['$S*1*'].e(0.5), poffx(1), shorten=(0,0.1))
eeftip += path(eeftip['$S*2*'].e(0.5), poffx(1), shorten=(0,0.1))
eeftip += path(eeftip['$S*{S_m}*'].e(0.5), poffx(1), shorten=(0,0.1)) 

fig << eeftip

fig << bus(p(ps['intercon'].e(), eeftip_axi_enter), eeftip_axi_enter, style=(bus_cap, '='))
fig << bus_text("AXI4").alignx(mid(ps.e(), eeftip.w()), prev().c()).aligny(fig[-1].pos(0.5), prev().s(0, 0.2))

#render_fig(fig, './system_bd.pdf')
