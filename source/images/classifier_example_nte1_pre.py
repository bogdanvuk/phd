from bdp import *
from classifier_example_nte_tmpl import nte, ports, fig
import copy
nte = copy.deepcopy(nte)
ports = copy.deepcopy(ports)

fig << '\definecolor{emphcolor}{RGB}{135,206,235}\n'
nte.text_t = "NTE$_1$"
nte['Coefficient*'].fill = 'emphcolor'
text_vals = text(margin=(0.3, 0.4), color='red')

for b in ['inst_inp_bus', 'cm_addr', 'cm_data']:
    ports[b].fill = 'emphcolor'

for b in ports['node_id_net']:
    ports['node_id_net'][b].fill = 'emphcolor'

for b in nte['mem_intf_net']:
    nte['mem_intf_net'][b].fill = 'emphcolor'

fig << text_vals(r"$\mathbf{x}=[\mathtt{4BE4},\mathtt{523D}]$ \\[2pt] $C = 2$", alignment='left').align(ports['inst_inp_bus'][-1], cur().n())
fig << text_vals(r"$\mathtt{0}$").align(ports['node_id_net'][0][-1], cur().n())
fig << text_vals(r"$\mathbf{w}=[\mathtt{4D2A},\mathtt{81D1}]$").align(ports['cm_data'][-1] + p(0, 1.2), cur().n())
fig << text_vals(r"$\mathtt{0}$").align(ports['cm_addr'][-1], cur().n())

fig << ports
fig << nte

# render_fig(fig)
