from bdp import *

comp = block(size=p(8,5), nodesep=(5,4), shape='ellipse')

fig << comp("Attributes")
fig << comp("Model", text_color='blue').right(fig["Attr"], 2)
fig << comp("Learning Algorithm", color='blue', text_color='blue').below(fig["Mod*"], 1)

fig << path(fig['Attr'].e(0.5), fig['Mod'].w(0.5), style=(None, '>'), thick=True)
fig << text("Instances").align(fig[-1].pos(0.5), prev().s(0.5))

fig << path(fig['Attr'].w(0.5), poffx(-8), style=('<', None), thick=True)
fig << text("Domain").align(fig[-1].pos(0.5), prev().s(0.5))
fig << text("objects").align(fig[-2].pos(0.5), prev().n(0.5))

fig << path(fig['Lea'].w(0.5), poffx(-8), style=('<', None), thick=True, color='blue')
fig << text("Training set", color='blue').align(fig[-1].pos(0.5), prev().s(0.5))

fig << path(fig['Lea'].n(0.5), fig['Mod'].s(0.5), style=(None, '>'), thick=True, color='blue')
fig << block("Learning problem", size=(18, 16),
             dotted=True, color='blue', thick=True,
             text_color='blue', text_margin=p(0.5, 0.5),
             alignment="sw").align(fig['Mod'].n(1.0) + p(1,-1), prev().n(1.0))

fig << block("Task", size=(22, 9),
             dotted=True, color='red', thick=True,
             text_color='red', text_margin=p(0.5, 0.5),
             alignment="nw").align(fig['Learning problem'].n(0) + p(1,-2), prev().n(0))

fig << path(fig['Mod'].e(0.5), poffx(8), style=(None, '>'), thick=True)
fig << text("Output").align(fig[-1].pos(0.5), prev().s(0.5))
