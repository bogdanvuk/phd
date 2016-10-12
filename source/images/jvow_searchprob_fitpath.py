from plot_searchprob_fitpath import plot_fitpath_comp, to_k
import os

# fns = ['../data/searchprob/jvow_fitpath_bare.js', '../data/searchprob/jvow_fitpath_norp.js',  '../data/searchprob/jvow_fitpath_hereboy.js']
# fns = ['fitpath_efti.js', 'fitpath_hereboy.js', 'fitpath_bare.js']
# fns = ['fitpath_efti.js', 'fitpath_hereboy.js']
fns = ['fitpath_bare.js', 'fitpath_subseq.js']
fns = [os.path.join(os.path.expandvars('$EFTI/script'), fn) for fn in fns]
# fns = [ '../data/searchprob/jvow_fitpath_bare.js', os.path.join(os.path.expandvars('$EFTI/script'), 'fitpath_norp.js'),]

plt = plot_fitpath_comp(fns, labels=['EFTI', 'Hereboy', 'Hill climbing'])

plt.gca().set_xlim([0,100000])
# plt.gca().set_ylim([0.10,0.30])
plt.gca().set_ylim([0.50,0.70])
plt.gca().xaxis.set_major_formatter(to_k)
plt.xlabel('iteration')
plt.ylabel('fitness')

plt.show()
