from pipeline_oper import plot_pipeline
from bdp import *

pipeline = plot_pipeline(slice(0,10))
fig << pipeline
#fig << block("", size=p(0,1), border=False).align(pipeline.e())
# render_fig(fig)
