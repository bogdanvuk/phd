import attrspace_plot
attr, cls = attrspace_plot.load_arff("../data/yingyang.csv")
ds = {'attr': attr, 'cls': cls}
attrspace_plot.plot(ds, (0,1), alpha=0.8)

#plt.gca().axes.get_xaxis().set_visible(False)
#plt.gca().axes.get_yaxis().set_visible(False)
plt.gca().set_ylabel('$x_1$')
plt.gca().set_xlabel('$x_2$')
plt.show()
#plt.savefig("oblique_dt_traversal_attrspace_only.pdf", bbox_inches='tight')
#plt.close()
