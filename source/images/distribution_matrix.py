from bdp import *

field = block(size=p(6,2))
bus_cap = cap(length=0.8, width=1.3, inset=0, type='Stealth')
bus = path(style=(bus_cap, bus_cap), line_width=0.7, double=True, border_width=0.1)

def make_row(pos, row_text, tmpl):
    tmpl.p = pos
    tmpl.left(tmpl, 0)
    objs = group()
    for t in row_text:
        tmpl.right(tmpl, 0)
        dotted = t.startswith("$\cdot") or (t == '')
        if t.startswith("$\cdot"):
            objs += tmpl(t, dotted=dotted, text_font='\\tiny')
        else:
            objs += tmpl(t, dotted=dotted)

    return objs

coef_row_text = []
for col_des in ['1', '2', 'N_l']:
    coef_row_text.append([
            '$d_{' + col_des + ',1}$',
            '$d_{' + col_des + ',2}$',
            '$\cdot\cdot\cdot$',
            '$d_{' + col_des + ',N_c}$'
    ])

coef_row_text.insert(2, [
                  r"$\cdot$ \\ $\cdot$ \\ $\cdot$",
                  r"$\cdot$ \\ $\cdot$ \\ $\cdot$",
                  '',
                  r"$\cdot$ \\ $\cdot$ \\ $\cdot$"
])

row_caption = [
    "Leaf ID 1",
    "Leaf ID 2",
    "",
    "Leaf ID $N_l$"
]

res_caption = [
    "$k_{1}, d_{(1,k_1)}$",
    "$k_{2}, d_{(2,k_2)}$",
    "",
    "$k_{N_l}, d_{(N_l,k_{N_l})}$"
]

col_caption = [
    "$C_{1}$",
    "$C_{2}$",
    "",
    "$C_{N_c}$"
]

pos = p(0,0)
coef_row = group()
for coef, caption, resc in zip(coef_row_text, row_caption, res_caption):
    if coef_row:
        pos = coef_row[-1][0].s(0)

    coef_row += make_row(pos, coef, field)
    fig << text(caption).align(coef_row[-1][0].w(0.5), prev().e(0.5))
    fig << bus(coef_row[-1][-1].e(0.5), poffx(2), shorten=p(0.4, 0), style=('', bus_cap))
    fig << text(resc).align(fig[-1][-1], cur().w(0.5))

for b,c in zip(coef_row[0], col_caption):
    fig << text(c).align(coef_row[0][b].n(0.5), cur().s(0.5))

fig << coef_row

# render_fig(fig)
