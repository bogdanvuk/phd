from bdp import *

task = block(size=p(1,2), alignment="tc", text_font='\\small', text_margin=p(0,0.15))
m_field = block('M',size=p(1.5,2), fill="white")
s_field = block('S',size=p(1.5,2), fill="white")
fig << "\\usetikzlibrary{patterns}\n"
fig << '\\definecolor{redpastel}{RGB}{235,130,130}\n'
fig << '\\definecolor{greenpastel}{RGB}{130,235,130}\n'
fig << '\\definecolor{bluepastel}{RGB}{135,206,235}\n'

iter = task(pattern="north west lines", size=p(6,2))
iter['M'] = m_field().align(iter.n(), cur().n())
iter['S'] = s_field().align(iter.e(), cur().e())

# def plot_ens_line(t_iter, ens_id, iter_cnt, ens_cnt):
#     ens = group()
#     ens['name'] = task("Ensemble {}".format(ens_id + 1), border=False)
#     ens['lineup'] = path(ens['name'].n(), poffx(30), dotted=True)
#     ens['linedown'] = path(ens['name'].s(), poffx(30), dotted=True)

#     ens['iters'] = group()
#     for i in range(iter_cnt):
#         ens['iters'] += t_iter("Iter {}".format(i + 1)).right(ens['name'], 1 + ens['name'].size[0]*(ens_id + ens_cnt*i))
#     return ens
def plot_ens_line(t_iter, ens_name, iter_names, iter_offsets):
    ens = group()
    ens['name'] = block(ens_name, size=p(6,2), border=False, alignment="ce")
    ens['lineup'] = path(ens['name'].n(), poffx(43), dotted=True)
    ens['linedown'] = path(ens['name'].s(), poffx(43), dotted=True)

    ens['iters'] = group()
    for n,o in zip(iter_names, iter_offsets):
        ens['iters'] += t_iter(n).right(ens['name'], o)
    return ens
ens_colors = ['redpastel', 'greenpastel', 'bluepastel']
ens_cnt = 3
iter_cnt = 2
ensemble = group()
for ens in range(ens_cnt):
    iter_names = ["Iter {}".format(i + 1) for i in range(iter_cnt)]
    iter_offsets = [1 + iter.size[0]*(ens + ens_cnt*i) for i in range(iter_cnt)]
    iter['M'].fill=ens_colors[ens]
    iter['S'].fill=ens_colors[ens]

    ensemble += plot_ens_line(iter, "Ensemble {}".format(ens + 1), iter_names, iter_offsets).align(p(0,ens*(1 + iter.size[1])))


iter_names = ["" for ens in range(ens_cnt) for i in range(iter_cnt)]
iter_offsets = [1 + iter.size[0]*(ens + ens_cnt*i) for ens in range(ens_cnt) for i in range(iter_cnt)]
cpu = plot_ens_line(iter, "Total", iter_names, iter_offsets).align(p(0,1+ensemble[-1].s()[1]))
for s in range(ens_cnt):
    for i in range(iter_cnt):
        cpu['iters'][s*iter_cnt + i]['M'].fill = ens_colors[s]
        cpu['iters'][s*iter_cnt + i]['S'].fill = ens_colors[s]

# iter_names = ["Ens {}, Iter {}".format(ens+1, i + 1) for ens in range(ens_cnt) for i in range(iter_cnt)]
iter_names = ["" for ens in range(ens_cnt) for i in range(iter_cnt)]
iter_offsets = [1 + iter.size[0]*(ens + ens_cnt*i) for ens in range(ens_cnt) for i in range(iter_cnt)]
cu_iter = iter(border=False)
del cu_iter.pattern
cu_iter['M'].text_t = ""
cu_iter['S'].text_t = ""
cu = plot_ens_line(cu_iter, "Control Unit", iter_names, iter_offsets).align(p(0,3+cpu.s()[1]))

for s in range(ens_cnt):
    for i in range(iter_cnt):
        cu['iters'][s*iter_cnt + i]['M'].fill = ens_colors[s]
        cu['iters'][s*iter_cnt + i]['S'].fill = ens_colors[s]

smae_task = task(size=p(3,2))
smae = group()
for s in range(ens_cnt):
    # iter_names = ["Iter {}".format(i + 1) for i in range(iter_cnt)]
    iter_names = ["" for i in range(iter_cnt)]
    iter_offsets = [1 + m_field.size[0] + iter.size[0]*(s + ens_cnt*i) for i in range(iter_cnt)]
    smae_task.fill=ens_colors[s]
    smae += plot_ens_line(smae_task, "SMAE {}".format(s + 1), iter_names, iter_offsets).align(p(0,1+cu.s()[1] + s*(1 + iter.size[1])))

for i in range(6):
    fig << path(ensemble[0]['name'].e()+p(1+i*iter.size[0],-2), smae[-1]['name'].e(1.0)+p(1+i*iter.size[0],2), color="black!30")

fig << ensemble
fig << text("CPU", font="\\Large").align(ensemble.n() - p(2, 0.5), cur().s())
fig << cpu
fig << cu
fig << text("EEFTIP", font="\\Large").align(cu.n() - p(2, 0.5), cur().s())
fig << smae
# render_fig(fig)
