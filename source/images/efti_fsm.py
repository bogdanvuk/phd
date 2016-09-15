from bdp import *

state = block(size=p(6, 3), shape='ellipse')

fig << state("Idle")
fig << state("Enqueue").align(fig["Idle"].c() + p(0, 6), cur().c())
fig << state("Flush").align(fig["Enqueue"].c() + p(0, 6), cur().c())
fig << state(r"Calculate \\ Accuracy").align(fig["Flush"].c() + p(0, 6), cur().c())

fig << path(fig["Idle"].s(0.5), fig["Enqueue"].n(0.5), style=('', '>'), shorten=p(0.2, 0.2))
fig << text("Start").align(fig[-1].pos(0.5), cur().w(0.5))
fig << path(fig["Enqueue"].s(0.5), fig["Flush"].n(0.5), style=('', '>'), shorten=p(0.2, 0.2))
fig << text("All enqueued").align(fig[-1].pos(0.5), cur().w(0.5))
fig << path(fig["Enqueue"].e(0.2) - p(0.1, -0.1), fig["Enqueue"].e(0.8) - p(0.1, 0.1), route=['to [out=330,in=30, looseness=6]'], style=('<', ''))
fig << text(r"Enqueue Next \\ Instance").align(fig['Enqueue'].e(0.5) + p(2.2, 0), cur().w(0.5))
fig << path(fig["Flush"].s(0.5), fig["Calculate*"].n(0.5), style=('', '>'), shorten=p(0.2, 0.2))
fig << text("All flushed").align(fig[-1].pos(0.5), cur().w(0.5))
fig << path(fig["Calculate*"].w(0.2) + p(0.1, -0.1), fig["Idle"].w(0.5), route=['to [out=210,in=180, looseness=0.5]'], style=('', '>'), shorten=p(0,0.3))

#render_fig(fig)
