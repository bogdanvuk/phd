from bdp import *
from classifier_example_nte_tmpl import nte, ports, fig, bus_text
import copy
nte = copy.deepcopy(nte)
ports = copy.deepcopy(ports)

fig << '\definecolor{emphcolor}{RGB}{135,206,235}\n'
nte.text_t = "NTE$_1$"

for b in [r"$\leq$", 'MUX1', 'MUX2']:
    nte[b].fill = 'emphcolor'

nte['Instance Queue'][2].fill = 'emphcolor'
nte['Instance Queue'][2].text_t = r"$[\mathtt{4BE4},\mathtt{523D}]$ \\[2pt] 2"
nte['Node Queue'][2].fill = 'emphcolor'
nte['Node Queue'][2].text_t = '0'
text_vals = text(margin=(0.3, 0.4), color='red')

# for g in ['add0']:
#     for e in nte[g]:
#         nte[g][e].fill = 'emphcolor'

for b in ['final_add_reg_bus', 'thr_reg_bus', 'chl_reg_bus', 'chr_reg_bus', 'node_id_mux', 'mux1_res_bus']:
    nte[b].fill = 'emphcolor'

for b in ['inst_out', 'node_id_out']:
    ports[b].fill = 'emphcolor'

fig << text_vals(r"$\mathtt{EE56}$").align(nte[r"$\leq$"].w(1) - p(1.5,0), cur().s(1.0))
fig << text_vals(r"$\mathtt{FA20}$").align(nte[r"$\leq$"].w(2) - p(1.5,0), cur().e(0.5))

fig << text_vals("$\mathtt{1}$").align(nte['MUX1'].s(1), cur().n(1.1, -0.2))
fig << text_vals("$\mathtt{0}$").align(nte['MUX1'].s(2), cur().n(-0.1, -0.2))
fig << text_vals(r"\textbf{true}").align(nte[r"$\leq$"].n(0.5), cur().s(0.5))
fig << text_vals("$\mathtt{1}$").align(nte[r"$\leq$"].e(0.5), cur().s())

fig << text_vals("$\mathtt{0}$").align(nte['msb_path'][0], cur().n())
fig << text_vals("$\mathtt{0}$").align(nte['MUX2'].e(0.5), cur().s())

fig << text_vals("$\mathtt{0}$").align(nte['MUX2'].s(1), cur().n(1.1, -0.2))
fig << text_vals("$\mathtt{0}$").align(nte['MUX2'].s(2), cur().n(-0.1, -0.2))

fig << text_vals(r"$\mathbf{x}=[\mathtt{4BE4},\mathtt{523D}]$ \\[2pt] $C = 2$", alignment='left').align(ports['inst_out'][-1], cur().n(1.0))
# fig << text_vals(r"$\mathbf{x}=[\mathtt{41FF},\mathtt{19FF}]$").align(ports['inst_out'][-1], cur().n(1.0))
fig << text_vals(r"$\mathtt{0}$").align(ports['node_id_out'][-1], cur().n(1.0))

fig << ports
fig << nte

# render_fig(fig)
