from bdp import *
from classifier_example_nte_tmpl import nte, ports, fig, bus_text
import copy
nte = copy.deepcopy(nte)
ports = copy.deepcopy(ports)

nte.text_t = "NTE$_2$"

text_vals = text(margin=(0.3, 0.4), color='red')

fig << text_vals(r"$\mathbf{x}=[\mathtt{41FF},\mathtt{19FF}]$").align(ports['inst_inp_bus'][-1], cur().n())
fig << text_vals(r"$\mathtt{0}$").align(ports['node_id_net'][0][-1], cur().n())
fig << text_vals(r"$\mathbf{w}=[\mathtt{4214},\mathtt{0995}]$").align(ports['cm_data'][-1] + p(0, 1.2), cur().n())
fig << text_vals(r"$\mathtt{0}$").align(ports['cm_addr'][-1], cur().n())

fig << text_vals(r"$\mathtt{1108E5EC}$").align(nte['mul'][0].n(1.0), cur().s())
fig << text_vals(r"$\mathtt{00F9186B}$").align(nte['mul'][1].s(1.0), cur().n())
fig << text_vals(r"$\mathtt{4214}$").align(nte['inp_coefs'][0].n(0.5) + p(0, 0.7), cur().s(0.5))
fig << text_vals(r"$\mathtt{41FF}$").align(nte['inp_coefs'][1].n(0.5) + p(0, 0.7), cur().s(0.5))
fig << text_vals(r"$\mathtt{0995}$").align(nte['inp_coefs'][2].n(0.5) + p(0, 0.7), cur().s(0.5))
fig << text_vals(r"$\mathtt{19FF}$").align(nte['inp_coefs'][3].n(0.5) + p(0, 0.7), cur().s(0.5))

fig << text_vals(r"$= \mathtt{14DF}$").align(nte[r"$\theta$"].e(0.5), cur().w(0.5))
fig << text_vals(r"$= \mathtt{0}$").align(nte[r"$ChL$"].e(0.5), cur().w(0.5))
fig << text_vals(r"$= \mathtt{80}$").align(nte[r"$ChR$"].e(0.5), cur().w(0.5))

fig << text_vals(r"$\mathtt{1108E5EC}$").align(nte['mul'][0].n(1.0), cur().s())
fig << text_vals(r"$\mathtt{00F9186B}$").align(nte['mul'][1].s(1.0), cur().n())
fig << text_vals(r"$\mathtt{1201fE57}$").align(nte['add0'][0].n(0.7), cur().s())

fig << text_vals(r"$\mathtt{1201}$").align(nte[r"$\geq$"].w(1) - p(1.5,0), cur().s(1.0))
fig << text_vals(r"$\mathtt{14DF}$").align(nte[r"$\geq$"].w(2) - p(1.5,0), cur().e(0.5))

fig << text_vals("$\mathtt{80}$").align(nte['MUX1'].s(1), cur().n(1.1, -0.2))
fig << text_vals("$\mathtt{0}$").align(nte['MUX1'].s(2), cur().n(-0.1, -0.2))
fig << text_vals(r"\textbf{false}").align(nte[r"$\geq$"].n(0.5), cur().s(0.5))
fig << text_vals("$\mathtt{0}$").align(nte[r"$\geq$"].e(0.5), cur().s())

fig << text_vals("0").align(nte['msb_path'][0], cur().n())
fig << text_vals("0").align(nte['MUX2'].e(0.5), cur().s())

fig << text_vals("80").align(nte['MUX2'].s(1), cur().n(1.1, -0.2))
fig << text_vals("0").align(nte['MUX2'].s(2), cur().n(-0.1, -0.2))

fig << text_vals(r"$\mathbf{x}=[\mathtt{41FF},\mathtt{19FF}]$", margin=(0, 0.1)).align(ports['inst_out'][-1], cur().n(1.0))
fig << text_vals(r"$80$").align(ports['node_id_out'][-1], cur().n(1.0))


fig << ports
fig << nte

#render_fig(fig)
