from bdp import *
from acc_calc_demo_plot import plot_calculator

dm = [ ["0"]*3 for _ in range(5)]
dm[3][0] = "1"

acc = plot_calculator(dm, slice(0,4), (3,0), 4)
fig << '\definecolor{emphcolor}{RGB}{135,206,235}\n'
fig << acc

# render_fig(fig)
