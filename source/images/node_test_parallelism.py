from bdp import *

elem = block(border=False, nodesep=p(0, 1), text_margin=p(0.05, 0))
circ = block(color="black!30", dashed=True, shape="ellipse")

arr_cap = cap(length=0.4, width=0.6, inset=0, type='Stealth')
arr = path(color="black!40", style=('', arr_cap), line_width=0.3, border_width=0.06, double=True)

na = 7

w = ['$w_{}$'.format(i+1) for i in range(na)]
x = ['$x_{}$'.format(i+1) for i in range(na)]
s1 = ['$S_{}$'.format(i+1) for i in range(na)]

pos = p(0,0)
wb = group()
xb = group()
pr = group()
add0 = group()
add1 = group()
add2 = group()
add3 = group()
s1b = group()
s2b = group()
s3b = group()

for wi, xi, s1i in zip(w, x, s1):
    wb += elem(wi).align(pos, cur().n())
    pr += elem("$\cdot$").right(wb[-1])
    xb += elem(xi).right(pr[-1])

    s1b += elem(s1i).below(pr[-1], 2).alignx(pr[-1].c(), cur().c())

    fig << circ(size=(xb[-1].s(1.0) - wb[-1].n() + p(0.1, 0.3))).align(pr[-1].c(), cur().c())
    fig << arr(pr[-1].c(), poffy(2), shorten=p(0.5, 0))

    if len(xb) < na:
        add0 += elem("+", text_color="black!20").right(xb[-1])
        pos = add0[-1].n(1.0)

        clr = "black" if len(xb) in [1, 3, 5] else "black!20"
        add1 += elem("+", text_color=clr).alignx(add0[-1].p).aligny(s1b[-1].c(), cur().c())

        if len(xb) in [2, 4, 6]:
            fig << circ(size=(s1b[-1].s(1.0) - s1b[-2].n() + p(0.5, 0.5))).align(add1[-2].c(), cur().c())
            fig << arr(add1[-2].c(), poffy(2), shorten=p(0.5, 0))
            s2b += elem("$S_{{{}{}}}$".format(len(xb)-1, len(xb))).below(add1[-2], 2).alignx(add1[-2].c(), cur().c())

            clr = "black" if len(xb) in [2, 6] else "black!20"
            add2 += elem("+", text_color=clr).alignx(add1[-1].p).aligny(s2b[-1].c(), cur().c())

    else:
        fig << arr(s1b[-1].c(), poffy(2), shorten=p(0.5, 0))
        s2b += elem("$S_7$").below(s1b[-1], 2)

for i in [0, 2]:
    fig << circ(size=(s2b[i+1].s(1.0) - s2b[i].n() + p(1, 1))).align(mid(s2b[i+1].s(1.0),s2b[i].n()), cur().c())
    fig << arr(add2[i].c(), poffy(2), shorten=p(0.5, 0))

s3b += elem("$S_{1234}$").below(add2[0], 2).alignx(add2[0].c(), cur().c())
s3b += elem("$S_{567}$").below(add2[2], 2).alignx(add2[2].c(), cur().c())

fig << circ(size=(s3b[1].s(1.0) - s3b[0].n() + p(1.5, 1.8))).align(mid(s3b[1].s(1.0),s3b[0].n()), cur().c())
add3 += elem("+").alignx(add2[1].p).aligny(s3b[-1].c(), cur().c())

for i, g in enumerate([add0, add1, add2, add3]):
    fig << text("Step {}".format(i+1)).alignx(wb[0].w() - p(1, 0), cur().e()).aligny(g[0].c(), cur().c())

from itertools import tee
def pairwise(iterable):
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)

for u, d in pairwise([add0, add1, add2, add3]):
    y = midy(u[0].c(), d[0].c())
    fig << path(p(wb[0].w()[0], y), p(xb[-1].e()[0], y), dotted=True)

for g in [wb, xb, pr, add0, add1, add2, add3, s1b, s2b, s3b]:
    fig << g

# render_fig(fig)
