from bdp import *

bit = block(size=(7,4), fill='white')

# fig << block(size=(30, 4), fill='white')
# fig << block(size=(30, 4), dashed=True, fill='white').align(fig[-1].n(-1,-1))

def make_reg(text, pos):
    reg = block(group='tight')
    reg += bit(text[0]).align(pos)
    reg += bit(text[1]).right(reg[-1], 0)
    reg += bit(r"$\cdot\cdot\cdot$").right(reg[-1], 0)
    reg += bit(text[2]).right(reg[-1], 0)
    reg += bit(text[3]).right(reg[-1], 0)
    
    return reg
# 
# fig << bit("EFTIP 31 Status Bit").align(fig[-1].n(-1,-1))
# fig << bit("EFTIP 30 Status Bit").right(fig[-1], 0)
# fig << bit(". . .").right(fig[-1], 0)
# fig << bit("EFTIP 1 Status Bit").right(fig[-1], 0)
# fig << bit("EFTIP 0 Status Bit").right(fig[-1], 0)

reg1 = make_reg(["$EFTIP_{{{0}}}$ Status Bit".format(i) for i in [32, 31, 2, 1]], (0,0))
regn = make_reg(["Unused", "Unused", "$EFTIP_{S_m}$ Status Bit", "$EFTIP_{S_m-1}$ Status Bit"], (0,8))


fig << reg1
fig << text("IRQ Status Word 0", align='right').left(reg1[0]).aligny(reg1[0].c(), prev().c())
fig << regn
fig << text(r"IRQ Status Word $\left \lceil \frac{S_m}{32} \right \rceil$", align='right').left(regn[0]).aligny(regn[0].c(), prev().c())

for i in [0, 1, 3, 4]:
    fig << text(r"$\cdot$ \\ $\cdot$ \\ $\cdot$").align(mid(reg1[i].c(), regn[i].c()), prev().c())
