from bdp.node import *

# mul_block = block("x", size=p(2,2), shape='circle')()
# bus([mul_block.n(0.25), mul_block.n(0.25) - (1,1)])()
# mul_block = block(size=p(2,2))()
# bus([mul_block.n(0.25), mul_block.n(0.25) + (0,5)])()



mul_block = block("x", size=p(2,2), shape='circle')
add_block = block("+", size=p(2,2), shape='circle')
 
mul = []

evaluator = block(dotted=True)
pin_leftx = evaluator.p[0] - 2

fifo_blk = block(size=p(4,4))
inst_fifo = []
inst_fifo.append(fifo_blk(t="$I_{i}$", size=p(6,4), p=evaluator.p + (13, 3))())
inst_fifo.append(fifo_blk(t="$I_{i+1}$").right(prev(1), 0)())
inst_fifo.append(fifo_blk(t="$I_{i+2}$").right(prev(1), 0)())
inst_fifo.append(fifo_blk(t="$\cdot\cdot\cdot$").right(prev(1), 0)())
# inst_fifo.append(fifo_blk(t="$I_{i+N_P-2}$").right(prev(1), 0)())
inst_fifo.append(fifo_blk(t="$I_{i+N_P-1}$").right(prev(1), 0)())
text("Instance Queue", margin=p(0,0)).align(inst_fifo[0].n(), prev().s())()

bus = path(double=True, thick=False)
bus_text = text(font="footnotesize", margin=p(0.4,0.2))

bus([p(pin_leftx, inst_fifo[0].w(0.5)[1]), inst_fifo[0].w(0.5)], style='->')()
bus_text(r"Instance \\ Input").align_y(prev(1)[1], prev().s()).align_x(evaluator.p)()

inp_coef_tmpl = block(size=p(3,2), border=False, text_align="ce", node_sep=(1, 0.5))
inp_coefs = []

inp_coefs.append(inp_coef_tmpl("$A_{1}$").below(inst_fifo[0], 1).align_x(inst_fifo[0].s(1.0) - (1,0), prev().s(1.0))())
inp_coefs.append(inp_coef_tmpl("$a_{1}$").below(prev(1))())
inp_coefs.append(inp_coef_tmpl("$A_{2}$").below(prev(1), 1)())
inp_coefs.append(inp_coef_tmpl("$a_{2}$").below(prev(1))())

inp_coefs.append(inp_coef_tmpl("$A_{N^{M}_{A}-1}$").below(prev(1), 2)())
inp_coefs.append(inp_coef_tmpl("$a_{N^{M}_{A}-1}$").below(prev(1))())
inp_coefs.append(inp_coef_tmpl("$A_{N^{M}_{A}}$").below(prev(1), 1)())
inp_coefs.append(inp_coef_tmpl("$a_{N^{M}_{A}}$").below(prev(1))())

for i in range(len(inp_coefs)//2):
    bus([inst_fifo[0].s(1), inp_coefs[2*i].w(0.5)], def_routing='|-', style='->')()

 
for i in range(len(inp_coefs)//2):
    mul.append(mul_block.align_y(mid(inp_coefs[2*i].p, inp_coefs[2*i+1].p)).align_x(inst_fifo[1].c(), mul_block.c())())
    path([inp_coefs[2*i].c(), mul[i].c()], shorten=(2, 1.5), style='->', thick=True)()
    path([inp_coefs[2*i+1].c(), mul[i].c()], shorten=(2, 1.5), style='->', thick=True)()
    
text(r"$\cdot$ \\ $\cdot$ \\ $\cdot$", font="normalsize").align_x(mul[1].c(), prev().c()).align_y(mid(mul[1].c(), mul[2].c()), prev().c())()
  
add = []

# small_reg_t = block(size=p(0.3, 1.5))

for i in range(len(mul)//2):
    add.append(add_block.align_y(mid(mul[2*i].p, mul[2*i+1].p)).align_x(inst_fifo[2].c(), add_block.c())())
    block(size=p(0.3, 1.2)).align(mid(add[i].c(), mul[2*i].c()), prev().c())()
    path([mul[2*i].c(), add[i].c()], shorten=(1.2, 2.8), style='->', thick=True)()
    path([mul[2*i].c(), add[i].c()], shorten=(2.8, 1.2), style='->', thick=True)()

#     bus([mul[2*i+1].c(), add[i].c()], shorten=(1.5, 1.5), style='->', thick=True)()
    block(size=p(0.3, 1.2)).align(mid(add[i].c(), mul[2*i+1].c()), prev().c())()
    path([mul[2*i+1].c(), add[i].c()], shorten=(1.2, 2.8), style='->', thick=True)()
    path([mul[2*i+1].c(), add[i].c()], shorten=(2.8, 1.2), style='->', thick=True)()
    

add.append(add_block.align_y(mid(add[0].p, add[1].p)).align_x(inst_fifo[-1].c(), add_block.c())())

for i in range(2):
    if i == 0:
        offset = (2.0, 1.2)
    else:
        offset = (2.0, -1.2)
    
    path([add[i].c(), add[i].c() + offset], shorten=(1.2, 0.5), style='->', thick=True)()
    path([add[-1].c() - offset, add[-1].c()], shorten=(0.5, 1.2), style='->', thick=True)()
    
    block(size=p(0.3, 1.5)).align(add[i].c() + offset, prev().c())()
    block(size=p(0.3, 2)).align(add[-1].c() - offset, prev().c())()

    text(t="$\cdot\cdot\cdot$", font="large").align(mid(add[i].c(), add[2].c()), prev().c())()
    
final_add_reg = block(size=p(0.3, 1.2)).align(add[2].c() + (2.0, 0), prev().c())()
path([add[-1].c(), final_add_reg.w(0.5)], shorten=(1.1, 0.1), style='->', thick=True)()

fifo_blk = block(size=p(4,3), conn_sep=1)

# struct_mem_reg = fifo_blk("REG").below(inp_coefs[7], 4).align_x(inst_fifo[-1].p)()

struct_mem_reg = block(size=(0.3, 6)).below(inp_coefs[7], 2).align_x(inst_fifo[-1].e(0), prev().c())()

node_fifo = []
node_fifo.append(fifo_blk(t="$N_{i}$", size=p(6,3)).below(struct_mem_reg, 3).align_x(inst_fifo[0].p)())
node_fifo.append(fifo_blk(t="$N_{i+1}$").right(prev(1), 0)())
node_fifo.append(fifo_blk(t="$N_{i+2}$").right(prev(1), 0)())
node_fifo.append(fifo_blk(t="$\cdot\cdot\cdot$").right(prev(1), 0)())
# node_fifo.append(fifo_blk(t="$N_{i+N_{P}-2}$").right(prev(1), 0)())
node_fifo.append(fifo_blk(t="$N_{i+N_{P}-1}$").right(prev(1), 0)())
text("Node Queue", margin=p(0,0)).align(node_fifo[0].n(), prev().s())()

for n, i in zip(node_fifo, inst_fifo):
    bus([i.s(1.0), n.n(1.0)], dotted=True)()

struct_mem_intf = block(r"Structural Memory Interface", size=p(6,6)).align(struct_mem_reg.c() - (4,0), prev().e(0.5))()
bus([node_fifo[-1].n(0.5), node_fifo[-1].n(0.5) - (0,1), struct_mem_intf.s(0.5)], def_routing='-|', style='->')()
bus_text("Node ID", margin=(1, 0.5)).align(prev(1)[2], prev().s())()
bus([struct_mem_intf.e(1), struct_mem_reg.w(1)], style='->')()
bus_text("$thr$").align(prev(1)[0], prev().s())()
bus([struct_mem_intf.e(3), struct_mem_reg.w(3)], style='->')()
bus_text(r"$ChL$").align(prev(1)[0], prev().s())()
bus([struct_mem_intf.e(5), struct_mem_reg.w(5)], style='->')()
bus_text(r"$ChR$").align(prev(1)[0], prev().s())()

addr_bus = bus([(pin_leftx, struct_mem_intf.w(2)[1]), struct_mem_intf.w(2)], style='<-')()
bus_text("SM addr").align_x(evaluator.p).align_y(struct_mem_intf.w(2), prev().s(0))()
data_bus = bus([(pin_leftx, struct_mem_intf.w(4)[1]), struct_mem_intf.w(4)], style='->')()
bus_text(r"SM data").align_x(evaluator.p).align_y(struct_mem_intf.w(4), prev().s(0))()

mem_intf = block(r"Coefficient Memory Interface", size=p(6,6)).align(mid(mul[0].c(), mul[-1].c()) - (10,0), prev().e(0.5))()
# bus([(pin_leftx, mem_intf.w(1)[1]), mem_intf.w(1)], style='->')()
# bus_text(r"Node ID").align_y(prev(1)[0], prev().s()).align_x(evaluator.p)()

addr_bus = bus([(pin_leftx, mem_intf.w(2)[1]), mem_intf.w(2)], style='<-')()
bus_text(r"CM addr", margin=(0.3, 0.4)).align_x(evaluator.p).align_y(mem_intf.w(2), prev().s(0))()
data_bus = bus([(pin_leftx, mem_intf.w(5)[1]), mem_intf.w(5)], style='->')()
bus_text(r"CM data", margin=(0.3, 0.4)).align_x(evaluator.p).align_y(mem_intf.w(5), prev().s(0))()

# bus([mem_intf.s(4), node_fifo[0].w(1)], def_routing='|-', style='->')()
# bus_text(r"Child \\ IDs").align(prev(1)[2], prev().s(1.0))()
# bus([mem_intf.s(3), node_fifo[0].w(2)], def_routing='|-', style='->')()
# bus_text(r"Leaf IDs").align(prev(1)[2], prev().s(1.0))()
# bus([mem_intf.e(5), node_fifo[0].n(1)], def_routing='-|', style='->')()
# bus_text("$threshold$").align(prev(1)[0], prev().s())()

# bus_text("child data: left ID, right ID").align(mem_intf.e(4) + (1,0), prev().n())()


for i in range(len(inp_coefs)//2):
    bus([mem_intf.e(3), mem_intf.e(3) + (1,0), inp_coefs[2*i+1].w(0.5)], def_routing='|-', style='->', dotted=True)()

bus([(pin_leftx, node_fifo[0].w(0.5)[1]), node_fifo[0].w(0.5)], style='->')()
bus([(pin_leftx, node_fifo[0].w(0.5)[1]), mem_intf.s(4)], def_routing='-|', style='->')()
bus_text(r"Node ID Input").align_y(prev(1)[0], prev().s()).align_x(evaluator.p)()

# bus([(pin_leftx, node_fifo[0].w(2)[1]), node_fifo[0].w(2)], style='->')()
# bus_text(r"Node Is Leaf Input").align_y(prev(1)[0], prev().n()).align_x(evaluator.p)()

comp = block("$\geq$", p(4,4), text_font="Large").right(add[-1], 4).align_y(add[-1].c(), prev().w(1))()
bus([final_add_reg.e(0.5), comp.w(1)], style='->', shorten=(0.3, 0))()
bus_text("$\sum_{i=1}^{n}a_{i}\cdot A_{i}$").align(comp.w(1) + (0.5,-1), prev().s(1.0))()

mux_tmpl = block("MUX1", p(4,4), text_font="large")

mux = mux_tmpl.right(comp, 2)()
bus_text("0").align(mux.s(1), prev().s(0.5))()
bus_text("1").align(mux.s(3), prev().s(0.5))()

bus([struct_mem_reg.e(1), struct_mem_reg.e(1) + (1.5,0), comp.w(3)], def_routing='|-', style='->')()
bus([struct_mem_reg.e(3), mux.s(1)], def_routing='-|', style='->')()
bus([struct_mem_reg.e(5), mux.s(3)], def_routing='-|', style='->')()

bus([comp.e(0.5), mux.w(0.5)], style='->')()

mux2 = mux_tmpl("MUX2").over(mux, 2).align_x(mux.e(), mux_tmpl.c())()
bus_text("0").align(mux2.s(1), prev().s(0.5))()
bus_text("1").align(mux2.s(3), prev().s(0.5))()
bus([mux.n(3), mux2.s(1)], style='->')()
bus([node_fifo[-1].e(0.5), mux2.s(3)], def_routing='-|', style='->')()
bus_text(r"Node ID").align(prev(1)[0], prev().s())()

# comp_zero = block("$MSB=1$", p(6,3), text_font="large").right(mux, 2)()
path([(mux2.s(3)[0], node_fifo[-1].e(0.5)[1]), (mux2.e(0.5)[0] + 6, node_fifo[-1].e(0.5)[1]),mux2.e(0.5)], def_routing='|-', style='->')()
bus_text(r"Node ID [MSB]").align_x(mux2.s(3), prev().s()).align_y(node_fifo[-1].e(0.5), prev().s())()
# bus([comp_zero.n(0.5), mux2.e(0.5)], def_routing='|-', style='->')()

evaluator.size[0] = (mux2.e() + (8, 0) - evaluator.p)[0]
evaluator.size[1] = (node_fifo[-1].s(1.0) + (1,1) - evaluator.p)[1]
evaluator("NTE", text_font="Large", text_align="nw")()

bus([mux2.n(0.5), p(evaluator.e()[0] + 2, mux2.n()[1] -2)], def_routing='|-', style='->')()
bus_text("Node ID Output").align_y(prev(1)[1], prev().s()).align_x(evaluator.e(), prev().s(1.0))()
# bus([mux.n(1), p(evaluator.e()[0] + 2, mux2.n()[1] -4)], def_routing='|-', style='->')()
# bus_text("Node ID Output").align_y(prev(1)[1], prev().s()).align_x(evaluator.e(), prev().s(1.0))()

bus([inst_fifo[-1].e(0.5), p(evaluator.e()[0] + 2, inst_fifo[-1].c()[1])], style='->')()
bus_text("Instance Output").align_y(prev(1)[1], prev().s()).align_x(evaluator.e(), prev().s(1.0))()
