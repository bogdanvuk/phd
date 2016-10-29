from bdp import *

field = block(size=p(6,3))
bus_cap = cap(length=0.4, width=0.6, inset=0, type='Stealth')
bus = path(color="black!80", style=('', bus_cap), line_width=0.3, border_width=0.06, double=True)


def make_row(pos, row_text, tmpl):
    tmpl.p = pos
    tmpl = tmpl.left(tmpl, 0)
    objs = group()
    for t in row_text:
        tmpl = tmpl.right(tmpl, 0)
        dotted = t.startswith("$\cdot") or (t == '')
        if t.startswith("$\cdot"):
            objs.append(tmpl(t, dotted=dotted, text_font="\\tiny"))
        else:
            objs.append(tmpl(t, dotted=dotted))

    return objs

coef_row_text = []
topo_row_text = []
for col_des in ['1', '2', 'N^{M}_{n}(l)']:
    coef_row_text.append([
            '$w_{' + col_des + ',1}$',
            '$w_{' + col_des + ',2}$',
            '$\cdot\cdot\cdot$',
            '$w_{' + col_des + ',N^{M}_{A}}$'
    ])
    topo_row_text.append([
            r'${\theta}_{' + col_des + '}$',
            '$ChL_{' + col_des + '}$',
#             '$LfL_{' + col_des + '}$',
            '$ChR_{' + col_des + '}$',
#             '$LfR_{' + col_des + '}$',
            ]
    )

coef_row_text.insert(2, [
                  r"$\cdot$ \\ $\cdot$ \\ $\cdot$",
                  r"$\cdot$ \\ $\cdot$ \\ $\cdot$",
                  '',
                  r"$\cdot$ \\ $\cdot$ \\ $\cdot$"
])

topo_row_text.insert(2, [
                  r"$\cdot$ \\ $\cdot$ \\ $\cdot$",
                  r"$\cdot$ \\ $\cdot$ \\ $\cdot$",
#                   r"$\cdot$ \\ $\cdot$ \\ $\cdot$",
#                   r"$\cdot$ \\ $\cdot$ \\ $\cdot$",
                  r"$\cdot$ \\ $\cdot$ \\ $\cdot$",
                  ])

row_caption = [
    "Node 1",
    "Node 2",
    "",
    "Node $N^{M}_{n}(l)$"
]


coef_row = group()
topo_row = group()

pos = p(0,0)
for coef, topo, caption in zip(coef_row_text, topo_row_text, row_caption):
    if coef_row:
        pos = coef_row[-1][0].s(0)

    coef_row.append(make_row(pos, coef, field))
    topo_row.append(make_row(coef_row[-1][-1].e(0) + (7.5,0), topo, field))
    fig << text(caption).align(coef_row[-1][0].w(0.5), prev().e(0.5))

fig << coef_row
fig << topo_row

addr_dec = block("User Port Interface Controller", topo_row[0][-1].s(1.0) + (3,0) - coef_row[0][0].n()).over(coef_row[0][0], 5)
fig << addr_dec

stripe_line = group()
stripe_line.append(path(coef_row[0][0].n() - (0, 4), coef_row[-1][0].s() + (0, 1), dotted=True))
stripe_text = ['32b Stripe',
            '$\cdot\cdot\cdot$',
               '$\cdot\cdot\cdot$',
               '$\cdot\cdot\cdot$',
               '32b Stripe',
               ]


stripe_line_span = (topo_row[0][-1].e() + (3,0) - coef_row[0][0].w())[0]/len(stripe_text)

for i in range(1, len(stripe_text)+1):
    stripe_line.append( path(stripe_line[i-1][0] + p(stripe_line_span, 0), stripe_line[i-1][1] + p(stripe_line_span, 0), dotted=True))
    fig << text(stripe_text[i-1]).alignx(mid(stripe_line[i][0], stripe_line[i-1][0]), prev().c()).aligny(coef_row[0][0].n() - (0,1.5), prev().c())
    fig << bus(fig[-1].c() - p(0,1.2), p(fig[-1].c()[0], addr_dec.s()[1]), style=(bus_cap, bus_cap), shorten=p(0, 0.2))

fig << stripe_line

fig << bus(addr_dec.e(0.5), addr_dec.e(0.5) + p(3, 0), style=(bus_cap, bus_cap), shorten = p(0.2, 0))
fig << text("User Port").align(fig[-1][-1], prev().s(1.0))

coef_brace = path(coef_row[-1][0].s() + (0, 0.5), coef_row[-1][-1].s(1.0) + (0, 0.5), decorate=True, decoration='{brace,amplitude=10pt,mirror}')
fig << coef_brace
topo_brace = path(topo_row[-1][0].s() + (0, 0.5), topo_row[-1][-1].s(1.0) + (0, 0.5), decorate=True, decoration='{brace,amplitude=10pt,mirror}')
fig << topo_brace

fig << bus(coef_row[-1][2].s(0) + (0,1.5), coef_row[-1][2].s(0) + (0,3), shorten = p(0.2, 0.2), style=(bus_cap, bus_cap))
cm_port_dec = block("CM Port Interface Controller", coef_row[0][-1].s(1.0) - coef_row[0][0].n()).align(coef_row[-1][2].s(0) + (0,3), prev().n(0.5))
fig << cm_port_dec

fig << bus(topo_row[-1][1].s(0.5) + p(0,1.5), topo_row[-1][1].s(0.5) + p(0,3), shorten = p(0.2, 0.2), style=(bus_cap, bus_cap))
sm_port_dec = block("SM Port Interface Controller", topo_row[0][-1].s(1.0) - topo_row[0][0].n()).align(topo_row[-1][1].s(0.5) + (0,3), prev().n(0.5))
fig << sm_port_dec

fig << bus(cm_port_dec.w(0.5), cm_port_dec.w(0.5) - (6, 0), style=(bus_cap, bus_cap), shorten = p(0.2, 0))
fig <<text("CM Port", margin=(0.5, 0.5)).align(fig[-1][-1], prev().s())

fig << bus(sm_port_dec.e(0.5), sm_port_dec.e(0.5) + (6, 0), style=(bus_cap, bus_cap), shorten = p(0.2, 0))
fig << text("SM Port", margin=(0.5, 0.5)).align(fig[-1][-1], prev().s(1.0))

#render_fig(fig)
