import dt2plot
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection

dt_def = {
    "0": {"lvl": 0, "id": 0,"cls": 0,"left": "1","right": "2","thr": 1,"coeffs": [2,0]},
    "1": {"lvl": 1, "id": 1,"cls": 0,"left": "3","right": "4","thr": -3,"coeffs": [8,-10]},
    "2": {"lvl": 1, "id": 2,"cls": 0,"left": "5","right": "6","thr": 1,"coeffs": [8,-10]},
    "3": {"lvl": 2, "id": 3,"cls": 1,"left": "-1","right": "-1","thr": 0.00000,"coeffs": []},
    "4": {"lvl": 2, "id": 4,"cls": 0,"left": "7","right": "8","thr": 7,"coeffs": [8,10]},
    "5": {"lvl": 2, "id": 5,"cls": 0,"left": "9","right": "10","thr": 11,"coeffs": [8,10]},
    "6": {"lvl": 2, "id": 6,"cls": 2,"left": "-1","right": "-1","thr": 0.00000,"coeffs": []},
    "7": {"lvl": 3, "id": 7,"cls": 1,"left": "-1","right": "-1","thr": 0.00000,"coeffs": []},
    "8": {"lvl": 3, "id": 8,"cls": 2,"left": "-1","right": "-1","thr": 0.00000,"coeffs": []},
    "9": {"lvl": 3, "id": 9,"cls": 1,"left": "-1","right": "-1","thr": 0.00000,"coeffs": []},
    "10": {"lvl": 3, "id": 10,"cls": 2,"left": "-1","right": "-1","thr": 0.00000,"coeffs": []}
}

eq_pos_def = {
    1: [0.40, 0.85],
    2: [-0.05, 0.36],
    3: [0.8, 0.63],
    5: [0.26, 0.40],
    7: [0.58, 0.58]
}

polygons_def = {
    1: [(0,0), (1,0), (1, 1), (0, 1)],
    2: [(0,0), (0.5,0), (0.5, 1), (0, 1)],
    5: [(0,0.3), (0.5,0.7), (0.5, 0), (0, 0)],
    8: [(0,0), (0.5,0), (0.5, 0.3), (0.25, 0.5), (0, 0.3)]
}

def plot_attrspace(dt, eq_pos, poly, poly_color, alpha):
    import os
    # print(os.getcwd())
    # print(os.path.abspath("source/data/yingyang.csv"))
    # dt2plot.plot(dt, "source/data/yingyang.csv", alpha=alpha)
    dt2plot.plot(dt, "/data/projects/phd/source/data/yingyang.csv", alpha=alpha)

    for i, c in eq_pos.items():
        plt.text(c[0], c[1], r"$\mathbf{w_{" + str(i) + r"}}\cdot \mathbf{x} - \theta_{" + str(i) + r"} = 0$", size=18)

    if poly:
        patches = []

        polygon = Polygon(poly, True)
        patches.append(polygon)

        p = PatchCollection(patches, cmap=matplotlib.cm.jet, alpha=0.1)
        p.set_facecolor(poly_color)

        plt.gca().add_collection(p)

    plt.tight_layout(rect=[0.05,0,0.95,1])
    return plt
