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

def figxy(x,y, fig):
    wmi,hmi = fig.bbox.get_points()[1]
    return x*wmi, y*hmi

def annotate(x,y, text, color, ax):
    ax.text(x, y, plt_func(x,y)+(0.03), text, size=20, color=color, alpha=0.8)
    # ax.scatter3D(x, y, plt_func(x,y)+0.03, color=None, s=10, alpha=0.8)

def axforpatch(x,y,dx,dy,ax,fig):
    wmi,hmi = fig.bbox.get_points()[1]
    wm,hm = fig.bbox_inches.get_points()[1]

    iax = inset_axes(ax,
                        width=dx*wm,
                        height=dy*hm,
                        bbox_to_anchor=(x*wmi,y*hmi)
                    )
    iax.axis("off")

    return iax

def figaddpatch(patch,x,y,width,height,ax,fig):
    iax = axforpatch(x,y,width,height,ax,fig)
    iax.add_patch(patch)

def circle(x,y,r,ax,fig,**kwargs):
    p = patches.Circle((0.5,0.5),0.3,**kwargs)
    figaddpatch(p, x+r/2, y+r/2, r*0.8,r,ax,fig)

def arrow(x,y,dx,dy,ax,fig,**kwargs):
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

    p = patches.Arrow(invx, invy, -1 if invx else 1, -1 if invy else 1, **kwargs)

    figaddpatch(p, x,y,dx,dy,ax, fig)

fig = plt.figure()
ax = fig.gca(projection='3d')

X = np.arange(-2.5, 4.5, 0.15)
Y = np.arange(-2.5, 4.5, 0.15)
X, Y = np.meshgrid(X, Y)
Z = plt_func(X,Y)
surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, color='w', edgecolor=(0.5, 0.5, 0.5), alpha=1, linewidth=0.05)

annotate(0.06,0.06, 'A', 'g', ax)
circle(0.391, 0.491, 0.012, ax, fig, color='g')
annotate(1.7,1.7, 'B', 'b', ax)
circle(0.530, 0.652, 0.012, ax, fig, color='b')
annotate(-0.2,-0.9, 'C', 'r', ax)
circle(0.351, 0.382, 0.012, ax, fig, color='r')
annotate(+2.6,-2.1, 'D', 'r', ax)
circle(0.454, 0.228, 0.012, ax, fig, color='r')

ax.set_axis_off()
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    plt.tight_layout(pad=0)

# bbox = Bbox.from_bounds(1, 1, 6, 3.5)
arrow(0.396, 0.486,0.035,-0.06,ax,fig, width=0.5, alpha=0.7)
arrow(0.386, 0.486,-0.035,-0.10,ax,fig, width=0.5, alpha=0.7, color='r')
plt.savefig("escape_local.pdf", bbox_inches='tight', pad=-1.4)
# plt.show()
