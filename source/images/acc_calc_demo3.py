from bdp import *
from acc_calc_demo_plot import plot_calculator, attr, cls, dt
import random
from dt_classify import classify

dm = [ ["0"]*3 for _ in range(5)]

random.seed(28)
for i in random.sample(range(len(attr)), 149):
    leaf = int(classify([float(a) for a in attr[i]], dt)['id'][1:])
    dm[leaf][int(cls[i])-1] = str(int(dm[leaf][int(cls[i])-1]) + 1)

acc = plot_calculator(dm, slice(148,150), (1,2), 4)
fig << '\definecolor{emphcolor}{RGB}{135,206,235}\n'
fig << acc

# render_fig(fig)
