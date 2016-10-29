from bdp import *

# task = block(size=p(1.5,2), alignment="tc", text_font='\\small', text_margin=p(0,0.15))
task = block(size=p(1.5,2), text_margin=p(0,0.15))
fig << "\\usetikzlibrary{patterns}\n"
fig << '\\definecolor{redpastel}{RGB}{235,130,130}\n'
fig << '\\definecolor{greenpastel}{RGB}{130,235,130}\n'
fig << '\\definecolor{bluepastel}{RGB}{135,206,235}\n'

# def plot_ens_line(t_iter, ens_name, iter_names, iter_offsets):
#     ens = group()
#     ens['name'] = block(ens_name, size=p(6,2), border=False, alignment="ce")
#     ens['lineup'] = path(ens['name'].n(), poffx(43), dotted=True)
#     ens['linedown'] = path(ens['name'].s(), poffx(43), dotted=True)

#     ens['iters'] = group()
#     for n,o in zip(iter_names, iter_offsets):
#         ens['iters'] += t_iter(n).right(ens['name'], o)
#     return ens

line_end = 48

def form_line(name, pos):
    elem = group(group='tight')
    elem['name'] = block(name, size=p(7,2), border=False, alignment="ce").align(pos)

    elem['lineup'] = path(elem['name'].n(), poffx(line_end), dotted=True)
    elem['linedown'] = path(elem['name'].s(), poffx(line_end), dotted=True)

    return elem

seg_names = ['M', 'S']
ens_colors = ['redpastel', 'greenpastel', 'bluepastel', 'redpastel']
iter_segments = [[2, 2, 2, 2, 1], [2, 2, 2, 2, 1], [2,2,2,1,0]]
smae_len = 5
ens_cnt = 3
iter_cnt = 5
ensemble = group()
for ens in range(ens_cnt):
    ensemble[ens] = form_line("EFTI {}".format(ens+1), p(0, ens*3))

    ensemble[ens]['segs'] = group()
    for i in range(iter_cnt):
        for s in range(iter_segments[ens][i]):
            if (i == 0) and (s==0):
                pos = ensemble[ens]['name'].e() + p(1+1.5*ens, 0)
            elif seg_names[s] == 'S':
                if i==0:
                    pos = ensemble[ens]['segs'][-1].e() + p(smae_len + 1.5*ens,0)
                else:
                    pos = ensemble[ens]['segs'][-1].e() + p(1.5*2*(ens_cnt - 1),0)
            else:
                pos = ensemble[ens]['segs'][-1].e()


            ensemble[ens]['segs'] += task(seg_names[s], fill=ens_colors[ens]).align(pos)

cpu = form_line("Combined", ensemble.s() + p(0, 1))
cpu['back'] = block(
    size=p(ensemble[ens_cnt-1]['segs'][-1].n(1.0)[0] - ensemble[0]['segs'][0].n()[0], 2),
    pattern="north west lines"
).align(cpu['name'].e()+p(1,0))

cpu['segs'] = group()
for ens in range(ens_cnt):
    for n in range(len(ensemble[ens]['segs'])):
        s = ensemble[ens]['segs'][n]
        cpu['segs'] += s().aligny(cpu['name'].n(), cur().n())

cu = form_line("Memory Access", cpu.s() + p(0, 3))
cu['segs'] = group()
for ens in range(ens_cnt):
    for n in range(len(ensemble[ens]['segs'])):
        s = ensemble[ens]['segs'][n]
        if n == 0:
            cu['segs'] += s(text_t="").aligny(cu['name'].n(), cur().n())
        elif n % 2:
            cu['segs'] += s(text_t="", size=p(3,2)).aligny(cu['name'].n(), cur().n())

smae = group()
for ens in range(ens_cnt):
    smae[ens] = form_line("EFTIP {} Acc.".format(ens+1), cu.s() + p(0,1 + ens*3))
    smae[ens]['segs'] = group()
    for n in range(len(ensemble[ens]['segs'])):
        s = ensemble[ens]['segs'][n]
        space_left = line_end - 1 - s.p[0]

        if space_left > 1:
            size = smae_len
            if space_left < smae_len:
                size = space_left - 1

            if s.text_t == 'M':
                smae[ens]['segs'] += block(size=p(size, 2), fill=ens_colors[ens]).aligny(smae[ens]['name'].n()).alignx(s.e())

fig << ensemble
fig << text("CPU", font="\\Large").align(ensemble.n() - p(2, 0.5), cur().s())
fig << cpu
fig << cu
fig << text("EEFTIP", font="\\Large").align(cu['name'].n() - p(2, 0.5), cur().s())
fig << smae

iters = 1
last_pos = ensemble[0]['name'].e()[0] + 1

for n in range(len(ensemble[ens]['segs'])):
    s = ensemble[ens_cnt-1]['segs'][n]

    if s.text_t == 'S':
        top = p(s.e()[0],ensemble[0]['name'].e()[1]-2)
        bottom = p(s.e()[0], smae[-1]['name'].e(1.0)[1] + 2)
        fig << path(bottom, top, color="black!30")

        fig << text('Iteration {}'.format(iters), font="\\large", margin=p(0, 0.5)).align(p(midx(last_pos, top), top[1] + 2), cur().s(0.5))
        iters += 1
        last_inter_pos = midx(last_pos, top) - last_pos
        last_pos = top[0]

fig << text('Iteration {}'.format(iters), font="\\large", margin=p(0, 0.5)).align(p(last_pos + last_inter_pos, top[1] + 2), cur().s(0.5))
fig << path(ensemble[0]['name'].e()+p(1,-2), smae[-1]['name'].e(1.0)+p(1,1), color="black!30")

# render_fig(fig)
