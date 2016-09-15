from pylab import *

# rc('text', usetex=True)

fig = plt.figure(figsize=(16,4), tight_layout=True)
plt.tick_params(axis='X', which='major', labelsize=18)

t = arange(1, 128, 1)
f = [real(10*x*x + 50000*x)/(20*x*x + 2000) for x in t]

tick_params(axis='both', which='major', labelsize=18)
plt = plot(t,f)

# gca().axes.get_yaxis().set_visible(False)
gca().spines['right'].set_visible(False)
gca().spines['top'].set_visible(False)
# gca().set_yticks([])
# gca().set_xticks([])
gca().set_ylabel("speedup", fontsize=20)
gca().set_xlabel("$n_e$", fontsize=30, multialignment = 'right')
gca().axes.get_xaxis().set_label_coords(1,-0.1)
# gca().spines['bottom'].capstyle = "projecting"
# print('speedup_func_plot')
# print(gca().spines['top'].__dict__)

al = 7 # arrow length in points
arrowprops=dict(clip_on=False, # plotting outside axes on purpose
    frac=1., # make end arrowhead the whole size of arrow
    headwidth=al, # in points
    facecolor='k')
kwargs = dict(  
                xycoords='axes fraction',
                textcoords='offset points',
                arrowprops= arrowprops,
             )

gca().annotate("",(1,0),xytext=(-al,0), **kwargs) # bottom spine arrow
gca().annotate("",(0,1),xytext=(0,-al), **kwargs) # left spin arrow

margins(0.03, 0.1)
xlim(1, 50)
gca().yaxis.grid(True)
gca().yaxis.set_major_locator(MultipleLocator(20))

show()
