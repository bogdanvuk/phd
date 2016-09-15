import numpy as np

dt = {
    "0": {"lvl": 0, "id": 0,"cls": 0,"left": "1","right": "2","thr": 1,"coeffs": [2,0]},
    "1": {"lvl": 1, "id": 1,"cls": 1,"left": "3","right": "4","thr": -1,"coeffs": [6, 5]},
    "2": {"lvl": 1, "id": 1,"cls": 1,"left": "5","right": "6","thr": -2,"coeffs": [6, 5]},
    "2": {"lvl": 1, "id": 2,"cls": 0,"left": "3","right": "4","thr": 0.10742,"coeffs": [0.18750,-0.00058]},
    "3": {"lvl": 2, "id": 3,"cls": 3,"left": "-1","right": "-1","thr": 0.00000,"coeffs": []},
    "4": {"lvl": 2, "id": 4,"cls": 2,"left": "-1","right": "-1","thr": 0.00000,"coeffs": []}
}

def find_dt_leaf_for_inst(dt, instance):

    cur_node = dt["0"]

    # Until a leaf is hit
    while (cur_node['left'] != '-1'):
        psum = np.dot(instance, cur_node['coeffs'])

        if psum < cur_node['thr']:
            cur_node = dt[cur_node['left']]
        else:
            cur_node = dt[cur_node['right']]

    return cur_node['cls']

def classify(dt, train_set):
    classes = []
    for i in train_set:
        classes.append(find_dt_leaf_for_inst(dt, i[:-1]))

    return classes
