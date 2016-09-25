import numpy as np
import matplotlib.pyplot as plt

def calc_acc(leaves, class_cnt, wo, fit):
    oversize = (leaves - class_cnt)/class_cnt
    return fit/(1 - wo*oversize*oversize)

class_cnt = 5
leaves = np.arange(2, 10, 0.1);
for ko in [0, 0.02, 0.1]:
    acc = np.array([calc_acc(x, class_cnt, ko, 0.8) for x in leaves])
    plt.plot(leaves, acc, linewidth=2)

plt.text(8, 0.79, "$K_o=0$", size=20)
plt.text(8, 0.817, "$K_o=0.02$", size=20)
plt.text(8, 0.87, "$K_o=0.1$", size=20)
plt.gca().set_ylabel('accuracy', size=12)
plt.gca().set_xlabel('$N_l$ - number of leaves', size=12)
plt.gca().set_ylim([0.77, 0.90])
plt.show()

# plt.savefig("pareto.pdf", bbox_inches='tight')
