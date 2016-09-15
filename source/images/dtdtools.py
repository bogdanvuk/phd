from bdp import *

templdef = {'node': block(size=p(2,2), shape='circle', nodesep=(0.3,1)),
            'leaf': block(size=p(2.8,1.8), nodesep=(0.3,1)),
            'path': path(shorten=(1.4, 1.6), style=('', '>'))
}


def dt_for_hw(node, level, nodes_per_level = [0]*3):
    if not node['c']:
        node['id'] = '8' + str(node['id'] - 1)
        del node['cls']
    else:
        node['id'] = nodes_per_level[level]
        nodes_per_level[level] += 1
        level += 1
        dt_for_hw(node['c'][0], level, nodes_per_level)
        dt_for_hw(node['c'][1], level, nodes_per_level)

def draw_children(bdp_node, dt_node, templ=templdef):

    node_templ = []
    if 'sep' in dt_node:
        sep = dt_node['sep']
    else:
        sep = 2

    for c, direction in zip(dt_node['c'], ['left', 'right']):
        node_templ = templ['node'] if c['c'] else templ['leaf']
        node_text = str(c['id']) if not 'cls' in c else '{}_$C_{{{}}}$'.format(c['id'], c['cls'])
        child_node = node_templ(str(c['id'])).below(bdp_node)
        child_node.alignx(bdp_node.c() + p((sep if direction == 'right' else -sep), 0), prev().c())

        if c['c']:
            draw_children(child_node, c, templ)

        bdp_node[direction] = child_node
        bdp_node['a'+direction] = templ['path'](bdp_node.c(), child_node.c())

def draw_dt(dt, templ=templdef):
    root = templ['node'](str(dt['id']))
    draw_children(root, dt, templ)
    return root

def find_width(node):
    tot_w = []
    for c in node['c']:
        warray = find_width(c)
        for i,w in enumerate(warray):
            while i >= len(tot_w):
                tot_w.append(0)

            tot_w[i] += w

    return [1] + tot_w

if __name__ == "__main__":
    from eftirun_findt import dt
    root = draw_dt(dt)
    fig << root
    render_fig(fig)
    print(fig)
