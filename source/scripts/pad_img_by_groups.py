import struct
import imghdr
from subprocess import call
import os

def get_image_size(fname):
    '''Determine the image type of fhandle and return its size.
    from draco'''
    with open(fname, 'rb') as fhandle:
        head = fhandle.read(24)
        if len(head) != 24:
            return
        if imghdr.what(fname) == 'png':
            check = struct.unpack('>i', head[4:8])[0]
            if check != 0x0d0a1a0a:
                return
            width, height = struct.unpack('>ii', head[16:24])

    return width, height

imgdir = "/data/projects/phd/source/images/efti_overview_dts"
imgs = [os.path.join(imgdir, "dot{0:02d}.png".format(i)) for i in range(8)]
groups = [ [0, 1, 2], [3, 4, 5], [6, 7]]
# groups = [ [0, 1, 2, 3, 4, 5, 6, 7]]
sizes = [get_image_size(i) for i in imgs]
print(sizes)
h_max = max(sizes, key=lambda x: x[1])[1]
w_max = max(sizes, key=lambda x: x[0])[0]

for g in groups:
    gh_max = max([sizes[i] for i in g], key=lambda x: x[1])[1]
    gw_max = max([sizes[i] for i in g], key=lambda x: x[0])[0]

    for i in g:
        call(["convert", imgs[i], "-gravity", "North", "-background", "rgb(255,255,255)", "-extent", "{}x{}".format(w_max, h_max), imgs[i]])
