import dt2plot
import attrspace_plot
import json

dataset = "../data/vene.csv"
jsfn = '/data/projects/phd/source/images/efti_overview_dts/json/415517.js'

with open(jsfn) as data_file:
    dt = json.load(data_file)

def region_ttl(i,c):
    if i == 4:
        v = 0x80
    elif i == 5:
        v = 0x81
    elif i == 6:
        v = 0x82
    elif i == 7:
        v = 0x83
    elif i == 8:
        v = 0x84

    return r'$\mathtt{{{}}}$'.format(hex(v)[2:])

plt = dt2plot.plot(dt, dataset, alpha=0.15, region_ttl=region_ttl)

plt.gca().axes.get_xaxis().set_visible(True)
plt.gca().axes.get_yaxis().set_visible(True)

inst = [0.5929, 0.6425]
cls = 2
plt.scatter(inst[0], inst[1], s=300, marker=attrspace_plot.markers[cls-1], facecolors=attrspace_plot.colors[cls-1], edgecolors=attrspace_plot.colors[cls-1], alpha=1)
plt.text(inst[0] - 0.085, inst[1] + 0.05, r'$\mathbf{{x}}=[{:.4f}, {:.4f}]$'.format(*inst), size=25)
plt.gca().set_ylabel('$x_2$', fontsize=20, rotation=0, labelpad=10)
plt.gca().set_xlabel('$x_1$', fontsize=20)

plt.show()
