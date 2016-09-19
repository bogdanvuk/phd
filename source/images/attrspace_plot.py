import matplotlib.pyplot as plt

markers = ['*', 's', 'o', '^', '*']
colors = ['r', 'g', 'b', 'b', 'b']


def load_arff(fn, class_col=-1):
    src = open(fn, 'r')

    attr = []
    cls = []

    for line in src:
        line = line.strip()

        if line:
            if not line[0] in ('@', '%'):
                entries = line.split(',')
                cls.append(entries[class_col])
                del entries[class_col]
                attr.append(entries)

    return attr, cls

def plot(ds, attri, alpha=1):

    import numpy as np

    class_marker = {}

    def partition_ds(ds, attri):
        partitions = {}
        for a, c in zip(ds['attr'], ds['cls']):
            if c not in partitions:
                partitions[c] = {'x': [], 'y': []}

            for name, pos in zip(['x', 'y'], attri):
                partitions[c][name].append(float(a[pos]))

        for c, p in partitions.items():
            for name, v in p.items():
                p[name] = np.array(v)

        return partitions

    s = len(ds['attr'])*[80]
    partitions = partition_ds(ds, attri)

    for i, (cls, p) in enumerate(sorted(partitions.items())):
        m = markers[i]
        c = colors[i]
        # print(np.amax(p['x']))
        # print(np.amax(p['y']))
        plt.scatter(p['x'], p['y'], s=s, marker=m, facecolors='none', edgecolors=c, alpha=alpha)

    #area = np.pi * (15 * np.random.rand(N))**2  # 0 to 15 point radiuses

    print('Ploting: {}, {}'.format(*attri))
    plt.ylim([0, 1])
    plt.xlim([0, 1])

def plot2pdf(ds, fn, attri, alpha=1):
    plot(ds, attri, alpha)
    plt.savefig(fn)
    plt.clf()
    plt.close()

if __name__ == "__main__":

    import itertools
    import time

    #attr, cls = load_arff("/data/personal/doktorat/data/data_sets_all/knowledge.csv")
    #attr, cls = load_arff("/data/personal/doktorat/data/data_sets_all/column_2C_weka.arff")
    #attr, cls = load_arff("/data/personal/doktorat/data/data_sets_all/iris.arff")
    attr, cls = load_arff("../data/yingyang.csv")
    ds = {'attr': attr, 'cls': cls}

    plot2pdf(ds, "attrspace.pdf", (0,1))
    # for c in itertools.combinations(range(len(ds['attr'][0])), 2):
    #    plot_dataset(ds, "attrspace.pdf", c)
    #    time.sleep(2)
