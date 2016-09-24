import matplotlib.pyplot as plt
import matplotlib
import attrspace_plot
import numpy as np
import math

attr, cls = attrspace_plot.load_arff("../data/vene.csv")
ds = {'attr': attr, 'cls': cls}

attrspace_plot.plot(ds, (0,1), alpha=0.1)

#inst_index = [69, 113]
inst_index = [69, 130]
delta = 0.4

inst = []
cls = []
for i in inst_index:
    inst.append(np.array( [ float(n) for n in ds['attr'][i]] ))
    cls.append(int(ds['cls'][i]))

plt.plot([a[0] for a in inst], [a[1] for a in inst], 'k--', linewidth=2)
for a, cls, t in zip(inst, cls, ['i', 'j']):
    plt.scatter(a[0], a[1], s=300, marker=attrspace_plot.markers[cls-1], facecolors=attrspace_plot.colors[cls-1], edgecolors=attrspace_plot.colors[cls-1], alpha=1)
    plt.text(a[0], a[1] + 0.05, r'$\mathbf{x}^' + t + '$', size=30)

w = np.subtract(inst[1], inst[0])

res = []
for a in inst:
    print(w, a)
    res.append(np.dot(w, a))

print(res)
thr = delta*res[1] + (1 - delta)*res[0]
print(thr)
y,x=np.ogrid[0:1:100j,0:1:100j]
plt.contour(x.ravel(), y.ravel(), w[0]*x + w[1]*y, [thr], linewidths=2, colors='k')
plt.text(0.45, 0.1, r'$H_{ij}(\mathbf{w},\theta)$', size=30)

dpos = np.add(delta/2*inst[1], (1-delta/2)*inst[0])
plt.text(dpos[0]-0.01, dpos[1] - 0.1, r'$\delta$', size=30)

dpos = np.add((1-(1-delta)/2)*inst[1], (1-delta)/2*inst[0])
plt.text(dpos[0] - 0.05, dpos[1] - 0.1, r'$1-\delta$', size=30, multialignment='center')

plt.xlabel('$x_1$', fontsize=20)
plt.ylabel('$x_2$', fontsize=20, rotation=0, labelpad=10)

#plt.contour(x.ravel(), y.ravel(), y + 0.0767853*x, [0.712073], linewidth=2)
#plt.show()
#plt.savefig("attrspace.pdf")
# plt.close()
#plot(ds, fn, attri):
