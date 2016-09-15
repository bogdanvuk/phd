from bdp import *

field = block(size=p(6,2))
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
for col_des in ['1', '2', 'N^{M}_{I}']:
    coef_row_text.append([
            '$x_{' + col_des + ',1}$',
            '$x_{' + col_des + ',2}$',
            '$\cdot\cdot\cdot$',
            '$x_{' + col_des + ',N^{M}_{A}}$',
            '$C_{' + col_des + '}$'
    ])

coef_row_text.insert(2, [
                  r"$\cdot$ \\ $\cdot$ \\ $\cdot$",
                  r"$\cdot$ \\ $\cdot$ \\ $\cdot$",
                  '',
                  r"$\cdot$ \\ $\cdot$ \\ $\cdot$",
                  r"$\cdot$ \\ $\cdot$ \\ $\cdot$"
])

row_caption = [
    "Instance 1",
    "Instance 2",
    "",
    "Instance $N^{M}_{I}$"
]


coef_row = group()

pos = p(0,0)
for coef, caption in zip(coef_row_text, row_caption):
    if coef_row:
        pos = coef_row[-1][0].s(0)

    coef_row.append(make_row(pos, coef, field))
    fig << text(caption).align(coef_row[-1][0].w(0.5), prev().e(0.5))

fig << coef_row
addr_dec = block("User Port Interface Controller", coef_row[0][-1].s(1.0) - coef_row[0][0].n()).over(coef_row[0][0], 5)
fig << addr_dec

stripe_line_span = (coef_row[0][-1].e() - coef_row[0][0].w())[0]/3

stripe_text = ['32b Stripe',
               '$\cdot\cdot\cdot$',
               '32b Stripe',
               ]

stripe_line = group()
stripe_headers = group()
stripe_line.append(path(coef_row[0][0].n() - (0, 4), coef_row[-1][0].s() + (0, 1), dotted=True))
for i in range(1, 4):
    stripe_line.append( path(stripe_line[i-1][0] + (stripe_line_span, 0), stripe_line[i-1][1] + (stripe_line_span, 0), dotted=True))
    stripe_headers.append(text(stripe_text[i-1]).alignx(mid(stripe_line[i][0], stripe_line[i-1][0]), prev().c()).aligny(coef_row[0][0].n() - (0,1), prev().s()))
    fig << bus(stripe_headers[-1].c() - p(0,1.2), p(stripe_headers[-1].c()[0], addr_dec.s()[1]), style=(bus_cap, bus_cap), shorten=p(0.2, 0))

fig << stripe_line
fig << stripe_headers

fig << bus(coef_row[-1][2].s(0.5) + p(0,1.5), coef_row[-1][2].s(0.5) + p(0,3), shorten = p(0.2, 0.2), style=(bus_cap, bus_cap))
nte_port_dec = block("NTE Port Interface Controller", coef_row[0][-1].s(1.0) - coef_row[0][0].n()).align(coef_row[-1][2].s(0.5) + (0,3), prev().n(0.5))
fig << nte_port_dec

fig << bus(addr_dec.e(0.5), addr_dec.e(0.5) + p(3, 0), style=(bus_cap, bus_cap))
fig << text("User Port").align(fig[-1][-1], cur().w(0.5))

fig << bus(nte_port_dec.e(0.5), nte_port_dec.e(0.5) + p(3, 0), style=(bus_cap, bus_cap))
fig << text("NTE Port").align(fig[-1][-1], prev().w(0.5))


fig << path(coef_row[-1][0].s() + (0, 0.5), coef_row[-1][-1].s(1.0) + (0, 0.5), decorate=True, decoration='{brace,amplitude=10pt,mirror}')

#render_fig(fig)
