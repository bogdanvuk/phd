import numpy as np
import matplotlib.pyplot as plt

def calc_acc(leaves, class_cnt, wo, fit):
    oversize = (leaves - class_cnt)/class_cnt
    return fit/(1 - wo*oversize)

class_cnt = 5
leaves = np.arange(2, 10, 0.1);
for i in range(3):
    acc = np.array([calc_acc(x, class_cnt, 0.1*i, 0.8) for x in leaves])
    plt.plot(leaves, acc)

plt.text(8, 0.81, "$K_o=0$", size=20)
plt.text(8, 0.88, "$K_o=0.1$", size=20)
plt.text(8, 0.97, "$K_o=0.2$", size=20)
plt.gca().set_ylabel('accuracy', size=12)
plt.gca().set_xlabel('$N_l$ - number of leaves', size=12)
plt.show()

#plt.savefig("pareto.pdf", bbox_inches='tight')
