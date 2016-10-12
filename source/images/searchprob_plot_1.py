from searchprob_plot import plot_searchprob 
plt = plot_searchprob(1000,
                    5e-5,
                    0.05,
                    dists = [0.4, 0.2, 0.1, 0.05, 0.01],
                    loc = "lower right",
                    aspect=0.6)

plt.show()
