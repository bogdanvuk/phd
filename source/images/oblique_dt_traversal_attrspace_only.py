import attrspace_plot
attr, cls = attrspace_plot.load_arff("../data/yingyang.csv")
ds = {'attr': attr, 'cls': cls}
plt = attrspace_plot.plot(ds, (0,1), alpha=0.8)

#plt.gca().axes.get_xaxis().set_visible(False)
#plt.gca().axes.get_yaxis().set_visible(False)
plt.gca().set_ylabel('$x_2$', fontsize=20, rotation=0, labelpad=10)
plt.gca().set_xlabel('$x_1$', fontsize=20)
plt.show()
#plt.savefig("oblique_dt_traversal_attrspace_only.pdf", bbox_inches='tight')
#plt.close()
