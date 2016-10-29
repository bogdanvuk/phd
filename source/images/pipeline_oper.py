from bdp import *
from dt_classify import classify
from dtdtools import dt_for_hw
from eftirun_findt import dt
import copy
import random
import attrspace_plot

pipstage = block(size=p(5.5,3.5), nodesep=p(0,0), text_margin=p(0,0))
bus_cap = cap(length=0.4, width=0.6, inset=0, type='Stealth')
bus = path(color="black!40", style=('', bus_cap), shorten=p(0.1,0.1), line_width=0.3, border_width=0.06, double=True)
inter_nte_space = 1.5
dt = copy.deepcopy(dt)
dt_for_hw(dt, 0)
import os
print(os.getcwd())
#fn = "/home/bvukobratovic/projects/rst/examples/doktorat/source/data/vene.csv"
fn = os.path.join(os.getcwd(), "source/data/vene.csv")
# fn = os.path.join(os.getcwd(), "../data/vene.csv")
attr, cls = attrspace_plot.load_arff(fn)

def coef2hex(val):
    return '{:04X}'.format(int(val) & (2**16-1))

def create_queue(qtext):
    queue = group(group="tight")
    for i in range(3):
        nte = block(group="tight")
        for j in range(3):
            stage_id = i*3 + j
            nte += pipstage(qtext[stage_id])

        for j in range(1,3):
            nte[j].align(nte[j-1].e(), nte[j].w())

        queue['nte{}'.format(i)] = nte
    # print(queue._render_tikz(fig))
    for i in range(1,3):
        queue[i].align(queue[i-1].e() + p(inter_nte_space,0), queue[i].w())
        queue += bus(queue[i-1].e(0.5), queue[i].w(0.5))

    queue += bus(queue[2].e(0.5), poffx(2))
    if qtext[-1] and qtext[-1] != '-':
        if r"\\" in qtext[-1]:
            queue += text(qtext[-1]).align(queue[-1].pos(0.1), cur().w(0.6))
        else:
            queue += text(qtext[-1]).align(queue[-1].path[-1], cur().w(0.5))

    queue += bus(queue[0].w(0.5) - p(2,0), queue[0].w(0.5))

    return queue

def plot_pipeline(w):
    random.seed(28)

    tset = [[float(a) for a in attr[i]] + [cls[i]] for i in reversed(random.sample(range(len(attr)), w.stop))]

    insttext = [r"$[\mathtt{{{}}}, \mathtt{{{}}}]$ \\[4pt] {}".format(*([coef2hex(xi*32768) for xi in x[:-1]] + [x[-1]]))
                for x in tset[w]]
    insttext += ['-'] * (10 - w.stop + w.start)

    # print(insttext)

    # return

    instname = ["$I_{{{}}}$".format(i) for i in reversed(range(w.start, w.stop))]
    instname += [''] * (10 - w.stop + w.start)

    nodetext = []
    for i in range(3):
        for j in range(3):
            set_id = i*3+j + w.start
            if set_id < w.stop:
                n = classify(tset[set_id][:-1], dt, max_level=i)
                nodetext.append(str(n['id']))
            else:
                nodetext.append('-')

    if w.stop - w.start > 9:
        n = classify(tset[set_id][:-1], dt)
        nodetext.append(str(n['id']))
    else:
        nodetext.append('')

    qinst = create_queue(insttext)
    if instname[-1]:
        qinst += text(instname[-1]).align(qinst[-2].n(0.5), cur().s(0.5))

    qnode = create_queue(nodetext)

    #pipeline = qnode
    pipeline = group(group="tight")
    pipeline += qinst
    pipeline += qnode.align(qinst[0].s() + p(0,2.5), qnode.n())

    for i in range(3):
        nte_size = qnode[0].s(1.0) - qinst[0].n() + p(inter_nte_space,4.5)
        pipeline += block(r"$NTE_{}$".format(i+1), size=nte_size, dotted=True, alignment="nc").align(qinst[i].n() - p(inter_nte_space/2, 3), cur().n())
        for j in range(3):
            stage_id = i*3 + j
            if instname[stage_id]:
                pipeline += text(instname[stage_id]).align(qinst[i][j].n(0.5), cur().s(0.5))

    pipeline += text("Instance Queue").align(qinst[0].s(), cur().n())
    pipeline += text("Node Queue").align(qnode[0].s(), cur().n())
    return pipeline

    # print(insttext)
    # print(nodetext)

#fig << plot_pipeline(slice(0,10))
#render_fig(fig)
# piptext = [
#     [
#         ("-", '0'),
#         ("-", '0'),
#         ("-", '0'),
#     ],
#     [
#         ("-", '0'),
#         ("-", '0'),
#         ("-", '0'),
#     ],
#     [
#         ("-", '0'),
#         ("-", '0'),
#         ("-", '0'),
#     ],
# ]

# inst_fifo = fifo_blk("Instance Queue")
# for i,t in enumerate(inst_fifo_text):
#     if i == 0:
#         inst_fifo += fifo_item(t, size=p(10,2))
#     else:
#         inst_fifo += fifo_item(t).right(inst_fifo[-1])

# nte += inst_fifo
