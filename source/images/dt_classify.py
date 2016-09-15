import numpy as np

def classify(inst, dt, max_level=float('inf')):
    node = dt
    level = 0
    while (node['c']):
        if level == max_level:
            break

        if np.dot(np.array(inst), np.array(node['w'])) < node['thr']:
            node = node['c'][0]
        else:
            node = node['c'][1]

        level += 1

    return node
