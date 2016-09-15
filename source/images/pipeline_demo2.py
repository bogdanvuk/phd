from pipeline_oper import plot_pipeline
from bdp import *

pipeline = plot_pipeline(slice(0,4))
fig << pipeline
fig << block("", size=p(3,1), border=False).align(pipeline.e())
#render_fig(fig)
