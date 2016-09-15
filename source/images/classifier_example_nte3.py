from bdp import *
from classifier_example_nte_tmpl import nte, ports, fig, bus_text
import copy
nte = copy.deepcopy(nte)
ports = copy.deepcopy(ports)

nte.text_t = "NTE$_3$"

text_vals = text(margin=(0.3, 0.4), color='red')

fig << text_vals(r"$\mathbf{x}=[\mathtt{41FF},\mathtt{19FF}]$").align(ports['inst_inp_bus'][-1], cur().n())
fig << text_vals(r"$\mathtt{80}$").align(ports['node_id_net'][0][-1], cur().n())

fig << text_vals("1").align(nte['msb_path'][0], cur().n())
fig << text_vals("1").align(nte['MUX2'].e(0.5), cur().s())

fig << text_vals("x").align(nte['MUX2'].s(1), cur().n(1.1, -0.2))
fig << text_vals("$\mathtt{80}$").align(nte['MUX2'].s(2), cur().n(-0.1, -0.2))

fig << text_vals(r"$\mathbf{x}=[\mathtt{41FF},\mathtt{19FF}]$", margin=(0, 0.1)).align(ports['inst_out'][-1], cur().n(1.0))
fig << text_vals(r"$\mathtt{80}$").align(ports['node_id_out'][-1], cur().n(1.0))

fig << ports
fig << nte

#render_fig(fig)
