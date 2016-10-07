from dt2plot import plot

dt = {
    "0": {"lvl": 0, "id": 0,"cls": 0,"left": "1","right": "2","thr": 0.145,"coeffs": [0.24533,-0.16081]},
    "1": {"lvl": 1, "id": 1,"cls": '?',"left": "-1","right": "-1","thr": 0.00000,"coeffs": []},
    "2": {"lvl": 1, "id": 2,"cls": '?',"left": "-1","right": "-1","thr": 0.00000,"coeffs": []}
    }

dataset = "../data/vene.csv"

plt = plot(dt, dataset, alpha=0.15)
plt.show()
