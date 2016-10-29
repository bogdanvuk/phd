from bdp import *

bus_cap = cap(length=0.4, width=0.6, inset=0, type='Stealth')
bus = path(color="black!80", style=('', bus_cap), line_width=0.3, border_width=0.06, double=True)
bus_text = text(font="\\footnotesize", margin=p(0.5,0.2))
origin = p(0,0)

def create_fitness_border(pos, name):
    if name:
        return block(name, size=p(18,11), p=pos, text_margin=(0.5,0), text_font='\\small', alignment='nw', fill='white')
    else:
        return block(name, size=p(18,11), p=pos, fill='white', dotted=True)

def create_fitness_block(pos, name):
    # bd = block(name, size=p(18,11), p=pos, text_margin=(0.5,0.5), text_font='\\small', alignment='nw', fill='white')
    bd = block(name, p=pos, text_margin=(0.5,0.5), text_font='\\small',
               alignment='nw', group='tight', group_margin=[p(1,2), p(1,1)])
    bd += block("Incrementer", size=p(7,3)).align(bd.n() + (1,2))
    bd += block("Dominant Class Calc.", size=p(7,3)).right(bd["Incr*"], 2)
    bd += block(r"Class Distribution \\ Memory", size=p(10, 3)).aligny(bd["Incr*"].s() + (0, 2)).alignx(mid(bd["Incr*"].c(), bd["Dominant*"].c()), prev().c())

    bd += bus(bd["Incr*"].s(5), bd["*Memory"].n(2), style=(bus_cap, bus_cap))
    bd += bus(bd["Dominant*"].s(2), bd["*Memory"].n(8), style=(bus_cap, bus_cap))

    return bd

acc = block("Accuracy Calculator", text_margin=p(0.5, 0.5), alignment="nw", dotted=True, group='tight', group_margin=[p(3,2), p(1,1)])

acc += create_fitness_block(origin, "$LDCC_1$")
acc += create_fitness_block(origin + (0,14), "$LDCC_{N^{M}_{l}}$")
for i in range(3):
    fig << text(r"$\cdot$ \\ $\cdot$ \\ $\cdot$", font="\\scriptsize").align(mid(acc[0].c(), acc[1].c()) + p(5,0)*(i - 1), prev().c())

leaf_id_in = acc[0]['Incr*'].w(1) - (8,0)
fig << path(leaf_id_in, acc[0]['Incr*'].w(1), style=('', bus_cap))
fig << bus_text("$Leaf\ ID$").align(leaf_id_in, prev().s())

class_in = acc[0]['Incr*'].w(2) - (8,0)
fig << path(class_in, acc[0]['Incr*'].w(2), style=('', bus_cap))
fig << bus_text("$C$").align(class_in, prev().s())

fig << path(acc[0]['Incr*'].w(1) - (2,0), acc[1]['Incr*'].w(1), routedef='|-', style=('', bus_cap))
fig << path(acc[0]['Incr*'].w(2) - (3,0), acc[1]['Incr*'].w(2), routedef='|-', style=('', bus_cap))

acc += block("Accuracy Provider", (5,17)).align(acc[0]['Dominant*'].n(1.0) + p(11,0))
fig << acc

# # mux_block = block("MUX", (4,8)).align(mid(acc[0].s(1.0), acc[1].n(1.0)) + (3,0), prev().w(0.5))()
# #

fig << path(acc[0]['Dominant*'].e(1), acc['*Provider'].w(1), style=('', bus_cap), routedef='|-')
fig << bus_text("$dominant\\_class_1$").align(acc['*Provider'].w(1), prev().s(1.0))
fig << path(acc[0]['Dominant*'].e(2), acc['*Provider'].w(2), style=('', bus_cap), routedef='|-')
fig << bus_text("$dominant\\_class\\_cnt_{1}$").align(acc['*Provider'].w(2), prev().n(1.0))

fig << path(acc[1]['Dominant*'].e(1), acc['*Provider'].w(15), style=('', bus_cap), routedef='|-')
fig << bus_text("$dominant\\_class_{N^{M}_{l}}$").align(acc['*Provider'].w(15), prev().s(1.0))
fig << path(acc[1]['Dominant*'].e(2), acc['*Provider'].w(16), style=('', bus_cap), routedef='|-')
fig << bus_text("$dominant\\_class\\_cnt_{N^{M}_{l}}$").align(acc['*Provider'].w(16), prev().n(1.0))


# # path([acc[1]['Dominant*'].e(0.5), acc[1]['Dominant*'].e(0.5) + (2,0), mux_block.w(7)], style='->', def_routing='|-')()
# fig << text(r"$\cdot$ \\ $\cdot$ \\ $\cdot$", font="\\footnotesize").align(acc['*Provider'].w(0.5) - (2,0), prev().c())
# #
# # sum_block = block("Sum Block", size=(7,8), alignment='nw').right(mux_block, 2).aligny(mux_block.c(), prev().c())()
# #
# # add_block = block("+", size=p(2,2), shape='circle')
# # add = add_block.align(sum_block.w(0.5) + (2,0), prev().c())()
# # reg = block(size=(2, 4)).right(add).aligny(add.c(), prev().c())()
# #
# # path([mux_block.e(0.5), add.w(0.5)], style='->')()
# # path([add.e(0.5), reg.w(0.5)], style='->')()
# # path([reg.s(0.5), reg.s(0.5) + (0,1), add.s(0.5)], def_routing = '-|', style='->')()
# #
# # # bus([acc[0]['Dominant*'].e(0.5), add.w(0.5)], style='->', shorten=(0,0.3))()
# # #
fig << path(acc['*Provider'].e(8), acc['*Provider'].e(8) + (5,0), style=('', bus_cap))
fig << bus_text("hits", margin=p(0.2,0.3)).align(acc['*Provider'].e(8) + (1,0), prev().s())
fig << bus(acc['*Provider'].e(10), acc['*Provider'].e(10) + (5,0), style=('', bus_cap))
fig << bus_text("dt\\_classes", margin=p(0.2,0.3)).align(acc['*Provider'].e(10) + (1,0), prev().s())
# bus([acc['*Provider'].e(9), acc['*Provider'].e(9) + (6,0)], style='->')()
# bus_text("dt\\_impurity").align(acc['*Provider'].e(9) + (1,0), prev().s())()

# render_fig(fig)
