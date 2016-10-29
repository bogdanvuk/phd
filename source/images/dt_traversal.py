from bdp import *

# bdp_config['grid'] = 8
text.font = 'footnotesize'
block.text_font = 'footnotesize'

# text("$\mathbf{a_{2}}\cdot \mathbf{A} < threshold_{2}$")()

fig.grid = 12
node = block(size=p(2,2), shape='circle', nodesep=(2,2))
leaf = block(size=p(2.8,1.8), nodesep=(1.8,1.8))

def draw_children_con(parent, children):
    fig << path(parent.c(), children[0].c(), shorten=(1.4, 1.6), style=('', '>'))
    fig << text("T").align(fig[-1].c(), prev().s(1.0))

    fig << path(parent.c(), children[1].c(), shorten=(1.4, 1.6), style=('', '>'))
    fig << text("F").align(fig[-1].c(), prev().s())

def draw_children(parent, templ, t, separation):
    objs = group()
    objs.add(templ[0](t[0]).below(parent).left(prev(), separation))
    objs.add(templ[1](t[1]).below(parent).right(prev(), separation))
    fig << objs
    return objs

def draw_node_test_eq(node, id, pos):
    t = "$T_{" + str(id) + "}(\mathbf{A})$"
    if pos == 'left':
        fig << text(t).align(node.w(0.5), prev().e(1.0))
    else:
        fig << text(t).align(node.e(0.5), prev().s())

root = node("1")

fig << root
draw_node_test_eq(root, 1, 'right')

root_ch = draw_children(root, [node, node], ['2', '3'], 2)
draw_node_test_eq(root_ch[0], 2, 'left')
draw_node_test_eq(root_ch[1], 3, 'right')
draw_children_con(root, root_ch)

node2_ch = draw_children(root_ch[0], [leaf, leaf], ['4-$C_{1}$', '5-$C_{2}$'], 1)
draw_children_con(root_ch[0], node2_ch)

node3_ch = draw_children(root_ch[1], [node, leaf], ['6', '7-$C_{3}$'], 1)
draw_node_test_eq(node3_ch[0], 6, 'right')
draw_children_con(root_ch[1], node3_ch)

node4_ch = draw_children(node3_ch[0], [leaf, leaf], ['8-$C_{4}$', '9-$C_{5}$'], 1)
draw_children_con(node3_ch[0], node4_ch)

# node5_ch = draw_children(node3_ch[1], [leaf, leaf], ['$C_{5}$', '$C_{6}$'], 1)
# draw_children_con(node3_ch[1], node5_ch)

fig << path(root.c(), root_ch[1].s(), node3_ch[0].c(), node4_ch[1].w(0.5), rounded_corners=10, thick=True, line_width=0.2, shorten=(0.5, 0.5), style=('', '>'), draw='red')

#render_fig(fig, './dt_traversal.pdf')
