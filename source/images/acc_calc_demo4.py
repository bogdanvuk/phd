from bdp import *
from acc_calc_demo_plot import plot_calculator, attr, cls, dt
import random
from dt_classify import classify

dm = [ ["0"]*3 for _ in range(5)]

random.seed(28)
for i in random.sample(range(len(attr)), 150):
    leaf = int(classify([float(a) for a in attr[i]], dt)['id'][1:])
    dm[leaf][int(cls[i])-1] = str(int(dm[leaf][int(cls[i])-1]) + 1)

acc = plot_calculator(dm, slice(148,150), None, 0, margin=[p(1,2), p(1,1)])

dc = [1, 2, 1, 0, 2]

for i in range(5):
    acc[0][i][dc[i]].fill = 'emphcolor'
    #acc[0][i][dc[i]].color="blue"
    #acc[0][i][dc[i]].ultra_thick=True

bus_cap = cap(length=0.4, width=0.6, inset=0, type='Stealth')
bus = path(color="black!80", style=('', bus_cap), line_width=0.3, border_width=0.06, double=True)
bus_text = text(font="\\scriptsize", margin=p(0,0.2))

fig << '\definecolor{emphcolor}{RGB}{135,206,235}\n'
fig << acc[0]
fig << path(acc[0].e(5), poffx(7), style=('', bus_cap))
fig << text("hits = {}".format(141), margin=p(0.2,0.3)).align(acc[0].e(5), prev().s())
fig << path(acc[0].e(7), poffx(7), style=('', bus_cap))
fig << text("dt\\_classes = [1, 1, 1]", margin=p(0.2,0.3)).align(acc[0].e(7), prev().s())

# render_fig(fig)
