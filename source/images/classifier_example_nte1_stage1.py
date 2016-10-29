from bdp import *
from classifier_example_nte_tmpl import nte, ports, fig
import copy
nte = copy.deepcopy(nte)
ports = copy.deepcopy(ports)

fig << '\definecolor{emphcolor}{RGB}{135,206,235}\n'
nte.text_t = "NTE$_1$"
nte['Instance Queue'][0].fill = 'emphcolor'
nte['Instance Queue'][0].text_t = r"$[\mathtt{4BE4},\mathtt{523D}]$ \\[2pt] 2"
nte['Node Queue'][0].fill = 'emphcolor'
nte['Node Queue'][0].text_t = '0'
text_vals = text(margin=(0.3, 0.4), color='red')

for g in ['coef_net', 'w_net', 'mul']:
    for e in nte[g]:
        nte[g][e].fill = 'emphcolor'

fig << text_vals(r"$\mathtt{16E00768}$").align(nte['mul'][0].n(1.0), cur().s())
fig << text_vals(r"$\mathtt{5776E0CD}$").align(nte['mul'][1].s(1.0), cur().n())
fig << text_vals(r"$\mathtt{4D2A}$").align(nte['inp_coefs'][0].n(0.5) + p(0, 0.7), cur().s(0.5))
fig << text_vals(r"$\mathtt{4BE4}$").align(nte['inp_coefs'][1].n(0.5) + p(0, 0.7), cur().s(0.5))
fig << text_vals(r"$\mathtt{81D1}$").align(nte['inp_coefs'][2].n(0.5) + p(0, 0.7), cur().s(0.5))
fig << text_vals(r"$\mathtt{523D}$").align(nte['inp_coefs'][3].n(0.5) + p(0, 0.7), cur().s(0.5))

fig << ports
fig << nte

# render_fig(fig)
