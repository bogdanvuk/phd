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
        sep = 1

    sep = sep*(templ['leaf'].size[0] + templ['leaf'].nodesep[0])/2

    for c, direction in zip(dt_node['c'], ['left', 'right']):
        node_templ = templ['node'] if c['c'] else templ['leaf']
        if ('cls' not in c) or (c['cls'] == 0):
            node_text = str(c['id'])
        else:
            node_text = '{}-$C_{{{}}}$'.format(c['id'], c['cls'])

        child_node = node_templ(node_text).below(bdp_node)
        child_node.alignx(bdp_node.c() + p((sep if direction == 'right' else -sep), 0), prev().c())

        if c['c']:
            draw_children(child_node, c, templ)

        bdp_node[direction] = child_node
        bdp_node['a'+direction] = templ['path'](bdp_node.c(), child_node.c())

def balance_dt(dt):
    dt['parent_dir'] = 0
    compute_seps(dt)

def draw_dt(dt, templ=templdef):
    root = templ['node'](str(dt['id']))
    draw_children(root, dt, templ)
    return root

MAX_HEIGHT = 1000
lprofile = [0] * MAX_HEIGHT
rprofile = [0] * MAX_HEIGHT
INFINITY = (1 << 20)

# adjust gap between left and right nodes
gap = 2

# The following function fills in the lprofile array for the given tree.
# It assumes that the center of the label of the root of this tree
# is located at a position (x,y).  It assumes that the sep
# fields have been computed for this tree.
def compute_lprofile(node, x, y):
    if node is None:
        return

    isleft = (node['parent_dir'] == -1)
    lprofile[y] = min(lprofile[y], x - ((1 - isleft) // 2))
    if node['c']:
        i = 1
        while (i <= node['sep'] and y + i < MAX_HEIGHT):
            lprofile[y + i] = min(lprofile[y + i], x - i)
            i += 1

        compute_lprofile(node['c'][0], x - node['sep']- 1, y + node['sep'] + 1)
        compute_lprofile(node['c'][1], x + node['sep'] + 1, y + node['sep'] + 1)


def compute_rprofile(node, x, y):
    if node is None:
        return

    notleft = (node['parent_dir'] != -1)
    rprofile[y] = max(rprofile[y], x + ((1 - notleft) // 2))
    if node['c']:
        i = 1
        while i <= node['sep'] and y + i < MAX_HEIGHT:
            rprofile[y + i] = max(rprofile[y + i], x + i)
            i += 1

        compute_rprofile(node['c'][0], x - node['sep'] - 1, y + node['sep'] + 1)
        compute_rprofile(node['c'][1], x + node['sep'] + 1, y + node['sep'] + 1)

# This function fills in the sep and
# height fields of the specified tree
def compute_seps(node):
    if node['c']:
        for n, d in zip(node['c'], [-1, 1]):
            n['parent_dir'] = d
            compute_seps(n)

    # now fill in the height of node
    h = 1

    # first fill in the sep of node
    if (not node['c']):
        node['sep'] = 0
    else:
        i = 0
        while (i < node['c'][0]['height'] and i < MAX_HEIGHT):
            rprofile[i] = -INFINITY
            i += 1
        compute_rprofile(node['c'][0], 0, 0)
        hmin = node['c'][0]['height']

        i = 0
        while (i < node['c'][1]['height'] and i < MAX_HEIGHT):
            lprofile[i] = INFINITY
            i += 1
        compute_lprofile(node['c'][1], 0, 0)
        hmin = min(node['c'][1]['height'], hmin)

        delta = 4
        i = 0
        while (i < hmin):
            delta = max(delta, gap + rprofile[i] - lprofile[i])
            i += 1

        # If the node has two children of height 1, then we allow the
        # two leaves to be within 1, instead of 2
        if (((node['c'][0]['height'] == 1) or (
                        node['c'][1]['height'] == 1)) and delta > 4):
            delta -= 1
        node['sep'] = ((delta + 1) // 2)

        h = max(node['c'][0]['height'] + node['sep'] + 1, h)
        h = max(node['c'][1]['height'] + node['sep'] + 1, h)

    node['height'] = h

if __name__ == "__main__":
    from eftirun_findt import dt
    dt['parent_dir'] = 0
    compute_seps(dt)
    print(dt)
    root = draw_dt(dt)
    fig << root
    render_fig(fig)
    print(fig)
