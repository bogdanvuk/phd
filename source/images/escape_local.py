from mpl_toolkits.mplot3d import Axes3D, proj3d
from matplotlib import cm
import matplotlib.patches as patches
from matplotlib.transforms import Bbox, BboxTransformTo, TransformedBbox
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axes_grid.inset_locator import inset_axes

def plt_func(X,Y):
    return np.exp(-(X**2 + Y**2)) + \
        0.5*np.exp(-((X-2)**2 + (Y+1.2)**2)) + \
        1.6*np.exp(-((X-1.7)**2 + (Y-1.7)**2))

def annotate(x,y, text, color, ax):
    ax.text(x, y, plt_func(x,y)+0.1, text, size=20, color=color, alpha=0.8)
    ax.scatter3D(x, y, plt_func(x,y)+0.03, color=color, s=10, alpha=0.8)

def arrow(x,y,dx,dy,ax,fig,**kwargs):
    wmi,hmi = fig.bbox.get_points()[1]
    wm,hm = fig.bbox_inches.get_points()[1]
    if dx < 0:
        dx = -dx
        invx = 1
    else:
        x = x + dx
        invx = 0

    if dy < 0:
        invy = 1
        dy = -dy
    else:
        y = y + dy
        invy = 0

    iax = inset_axes(ax,
                        width=dx*wm,
                        height=dy*hm,
                        bbox_to_anchor=(x*wmi,y*hmi)
                    )
    iax.axis("off")
    # iax.arrow(invx, invy, -1 if invx else 1, -1 if invy else 1, **kwargs)
    iax.add_patch(
        patches.Arrow(invx, invy, -1 if invx else 1, -1 if invy else 1, **kwargs)
    )

# def draw(x,y,w,h,ax,fig):
#     # x2, y2, _ = proj3d.proj_transform(x,y,z, ax.get_proj())
#     wm,hm = fig.bbox.get_points()[1]
#     iax = inset_axes(ax,
#                         width=w,
#                         height=h,
#                         bbox_to_anchor=(x*wm,y*hm)
#                     )
#     iax.axis("off")
#     iax.arrow(int(not invx), int(not invy), invx, invy)

fig = plt.figure()
ax = fig.gca(projection='3d')

X = np.arange(-2.5, 4.5, 0.15)
Y = np.arange(-2.5, 4.5, 0.15)
X, Y = np.meshgrid(X, Y)
# R = np.sqrt(X**2 + Y**2)
Z = plt_func(X,Y)
surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, color='w', edgecolor=(0.5, 0.5, 0.5), alpha=1, linewidth=0.05)

annotate(0,0, 'A', 'b', ax)
annotate(1.7,1.7, 'B', 'r', ax)
ax.set_axis_off()
plt.tight_layout(pad=0)

# plt.margins(0,0)
# arrow(0.5,0.5,-0.1,0.1,ax,fig, head_width=0.05, head_length=0.1, fc='k', ec='k')
bbox = Bbox.from_bounds(1, 1, 6, 3.5)
arrow(0.39, 0.512,0.05,-0.06,ax,fig, width=0.5, alpha=0.7)
plt.show()
# plt.savefig("escape_local.pdf", bbox_inches=bbox)
# plt.savefig("escape_local.pdf", bbox_inches='tight', pad_inches=-1)
