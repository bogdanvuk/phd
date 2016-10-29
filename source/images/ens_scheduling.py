from bdp import *

task = block(size=p(1,2), alignment="tc", text_font='\\small', text_margin=p(0,0.15))
m_field = block('M',size=p(1.5,2), fill="white")
s_field = block('S',size=p(1.5,2), fill="white")
fig << "\\usetikzlibrary{patterns}\n"
fig << '\\definecolor{redpastel}{RGB}{235,130,130}\n'
fig << '\\definecolor{greenpastel}{RGB}{130,235,130}\n'
fig << '\\definecolor{bluepastel}{RGB}{135,206,235}\n'

smae_len = 5
t_iter = task(pattern="north west lines", size=p(smae_len+2*1.5, 2))
t_iter['M'] = m_field().align(t_iter.n(), cur().n())
t_iter['S'] = s_field().align(t_iter.e(), cur().e())

line_end = 48

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
    ens['name'] = block(ens_name, size=p(7,2), border=False, alignment="ce")
    ens['lineup'] = path(ens['name'].n(), poffx(line_end), dotted=True)
    ens['linedown'] = path(ens['name'].s(), poffx(line_end), dotted=True)

    ens['iters'] = group()
    for n,o in zip(iter_names, iter_offsets):
        if o < line_end - ens['name'].size[0] - 1:
            ens['iters'] += t_iter(n).right(ens['name'], o)

    return ens

ens_colors = ['redpastel', 'greenpastel', 'bluepastel']
ens_cnt = 3
iter_cnt = 2
ensemble = group()
for ens in range(ens_cnt):
    # iter_names = ["Iter {}".format(i + 1) for i in range(iter_cnt)]
    iter_names = ["" for i in range(iter_cnt)]
    iter_offsets = [1 + t_iter.size[0]*(ens + ens_cnt*i) for i in range(iter_cnt)]
    t_iter['M'].fill=ens_colors[ens]
    t_iter['S'].fill=ens_colors[ens]

    ensemble += plot_ens_line(t_iter, "EFTI {}".format(ens + 1), iter_names, iter_offsets).align(p(0,ens*(1 + t_iter.size[1])))


iter_names = ["" for ens in range(ens_cnt) for i in range(iter_cnt)]
iter_offsets = [1 + t_iter.size[0]*(ens + ens_cnt*i) for ens in range(ens_cnt) for i in range(iter_cnt)]
cpu = plot_ens_line(t_iter, "Combined", iter_names, iter_offsets).align(p(0,1+ensemble[-1].s()[1]))
for s in range(ens_cnt):
    for i in range(iter_cnt):
        index = s*iter_cnt + i
        if index < len(cpu['iters']):
            cpu['iters'][index]['M'].fill = ens_colors[s]
            cpu['iters'][index]['S'].fill = ens_colors[s]

# iter_names = ["Ens {}, Iter {}".format(ens+1, i + 1) for ens in range(ens_cnt) for i in range(iter_cnt)]
iter_names = ["" for ens in range(ens_cnt) for i in range(iter_cnt)]
iter_offsets = [1 + t_iter.size[0]*(ens + ens_cnt*i) for ens in range(ens_cnt) for i in range(iter_cnt)]
cu_iter = t_iter(border=False)
del cu_iter.pattern
cu_iter['M'].text_t = ""
cu_iter['S'].text_t = ""
cu = plot_ens_line(cu_iter, "Memory Access", iter_names, iter_offsets).align(p(0,3+cpu.s()[1]))

for s in range(ens_cnt):
    for i in range(iter_cnt):
        index = s*iter_cnt + i
        if index < len(cpu['iters']):
            cu['iters'][index]['M'].fill = ens_colors[s]
            cu['iters'][index]['S'].fill = ens_colors[s]

smae_task = task(size=p(smae_len,2))
smae = group()
for s in range(ens_cnt):
    # iter_names = ["Iter {}".format(i + 1) for i in range(iter_cnt)]
    iter_names = ["" for i in range(iter_cnt)]
    iter_offsets = [1 + m_field.size[0] + t_iter.size[0]*(s + ens_cnt*i) for i in range(iter_cnt)]
    smae_task.fill=ens_colors[s]
    smae += plot_ens_line(smae_task, "EFTIP {} Acc.".format(s + 1), iter_names, iter_offsets).align(p(0,1+cu.s()[1] + s*(1 + t_iter.size[1])))

protrude = [2, 0, 0, 2, 0, 0]
for i in range(6):
    fig << path(ensemble[0]['name'].e()+p(1+i*t_iter.size[0],-protrude[i]), smae[-1]['name'].e(1.0)+p(1+i*t_iter.size[0],2), color="black!30")

for i in range(iter_cnt):
    s = ensemble[ens_cnt//2]['iters'][i]
    fig << text('Iteration {}'.format(i+1), font="\\large", margin=p(0, 0.5)).align(s.n(0.5) - p(0,3), cur().s(0.5))

fig << ensemble
fig << text("CPU", font="\\Large").align(ensemble.n() - p(2, 0.5), cur().s())
fig << cpu
fig << cu
fig << text("EEFTIP", font="\\Large").align(cu.n() - p(2, 0.5), cur().s())
fig << smae
# render_fig(fig)
