from bdp import *
import random
import attrspace_plot
from dt_classify import classify
from dtdtools import dt_for_hw
from eftirun_findt import dt
import copy

dt = copy.deepcopy(dt)
dt_for_hw(dt, 0)
import os
print(os.getcwd())
#fn = "/home/bvukobratovic/projects/rst/examples/doktorat/source/data/vene.csv"
fn = os.path.join(os.getcwd(), "source/data/vene.csv")
#fn = os.path.join(os.getcwd(), "../data/vene.csv")
attr, cls = attrspace_plot.load_arff(fn)

cell = block(size=p(3,2), nodesep=p(0,0), text_margin=p(0,0))
t_list_block = block(size=p(2,3), nodesep=p(0,0), text_margin=p(0,0))

def create_fitness_block(name, row):
    bd = block(name, text_margin=p(0.5, 0.5), alignment="nw", dotted=True, group='tight', group_margin=[p(1,2), p(0,0)])
    for i in range(3):
        bd += cell(row[i])

    for i in range(1, 3):
        bd[i].align(bd[i-1].e(), bd[i].w())
                    
    return bd

def classification_list(w, list_len):
    random.seed(28)
    inst_sel = random.sample(range(len(attr)), w.stop)
    tset = [[float(a) for a in attr[i]] + [cls[i]] for i in inst_sel]
    cl = [str(classify(tset[set_id][:-1], dt)['id']) for set_id in range(w.start, w.stop)]
    list_block = group()

    for i in range(list_len - w.stop + w.start):
        list_block[str(i)] = t_list_block("")
    
    for l, c in zip(reversed(cl), [tset[i][-1] for i in reversed(range(w.start, w.stop))]):
        list_block += t_list_block(r"$\mathtt{{{}}}$ \\ {}".format(l, c))

    for b in range(1, len(list_block)):
        list_block[b].align(list_block[b-1].e(), list_block[b].w())

    for b in range(w.start, w.stop):
        list_block += block("$I_{{{}}}$".format(b), border=False).align(list_block[list_len - b + w.start - 1].n(0.5), cur().s(0.5))
        
    return list_block

def plot_calculator(dm, w, highlight, list_len, margin=[p(3,2), p(1,1)]):

    img = group()
    
    acc = block("Accuracy Calculator", text_margin=p(0.5, 0.5), alignment="nw", dotted=True, group='tight', group_margin=margin)
    for i in range(5):
        acc += create_fitness_block("$LDCC_{}$".format(i), dm[i])
        
    for i in range(1,5):
        acc[i].align(acc[i-1].s() + p(1, 2), acc[i].n())

    if list_len:
        cl = classification_list(w, list_len)
        cl.align(acc.w(0.5) - p(1,0), cl.e())

        leaf_net = net()
        cls_net = net()
        for i in range(5):
            leaf_net += path(cl.e(1), poffx(2), acc[i].w(2), routedef='|-', style=('', '>'))
            cls_net += path(cl.e(2), poffx(3), acc[i].w(3), routedef='|-', style=('', '>'))

        leaf_net[highlight[0]].line_width=0.2
        leaf_net[highlight[0]].color='blue'
        cls_net[highlight[0]].line_width=0.2
        cls_net[highlight[0]].color='blue'
        #leaf_net += path(cl.e(1), poffx(2), acc[3].w(2), routedef='|-', style=('', '>'), line_width=0.2, color="blue")
        #cls_net += path(cl.e(2), poffx(3), acc[3].w(3), routedef='|-', style=('', '>'), line_width=0.2, color="blue")

        #        acc[highlight[0]][highlight[1]].very_thick=True
        acc[highlight[0]][highlight[1]].fill = 'emphcolor'
#        acc[highlight[0]][highlight[1]].color="blue"
#        acc[highlight[0]][highlight[1]].dotted = False
    
        acc[highlight[0]].very_thick="blue"
        acc[highlight[0]].color="blue"
        acc[highlight[0]].dotted = False

    img += acc

    if list_len:
        img += cl

        if list_len == w.stop - w.start:
            img += text("$\cdot\cdot\cdot$", font="\\large").align(cl[0].w(0.5), cur().e(0.5))
            img += path(cl.n(), cl.s(), color="white")
            img += path(cl.n(1.0), cl.s(1.0), color="white")

        img += leaf_net
        img += cls_net
    
    return img
