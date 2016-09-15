from bdp import *
from classifier_example_nte_tmpl import nte, ports, fig, bus_text
import copy
nte = copy.deepcopy(nte)
ports = copy.deepcopy(ports)

fig << '\definecolor{emphcolor}{RGB}{135,206,235}\n'
nte.text_t = "NTE$_1$"
nte['Structural*'].fill = 'emphcolor'
nte['Instance Queue'][1].fill = 'emphcolor'
nte['Instance Queue'][1].text_t = r"$[\mathtt{41FF},\mathtt{19FF}]$"
nte['Node Queue'][1].fill = 'emphcolor'
nte['Node Queue'][1].text_t = '0'
text_vals = text(margin=(0.3, 0.4), color='red')

for g in ['add0']:
    for e in nte[g]:
        nte[g][e].fill = 'emphcolor'

for p in ['node_id_sm_bus', 'chr_bus', 'chl_bus', 'thr_bus']:
    nte[p].fill = 'emphcolor'

for p in ['sm_addr', 'sm_data']:
    ports[p].fill = 'emphcolor'

fig << text_vals(r"$= \mathtt{FA20}$").align(nte[r"$\theta$"].e(0.5), cur().w(0.5))
fig << text_vals(r"$= \mathtt{0}$").align(nte[r"$ChL$"].e(0.5), cur().w(0.5))
fig << text_vals(r"$= \mathtt{1}$").align(nte[r"$ChR$"].e(0.5), cur().w(0.5))

fig << text_vals(r"$\mathtt{13E486D6}$").align(nte['mul'][0].n(1.0), cur().s())
fig << text_vals(r"$\mathtt{732FB82F}$").align(nte['mul'][1].s(1.0), cur().n())
fig << text_vals(r"$\mathtt{07143F05}$").align(nte['add0'][0].n(0.7), cur().s())

fig << ports
fig << nte

#render_fig(fig)
