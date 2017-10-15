from matplotlib.textpath import TextPath
from matplotlib.patches import PathPatch
from matplotlib.colors import to_rgba

from matplotlib.transforms import Affine2D, Bbox

import numpy as np
import pdb

class Character:
    def __init__(self, c, xmin, ymin, width, height, color,
                 font_properties=None,
                 flip=False,
                 shade=1,
                 alpha=1, edgecolor='none'):
        assert width > 0
        assert height > 0

        self.c = c
        self.bbox = Bbox.from_bounds(xmin,ymin,width,height)
        self.font_properties = font_properties
        self.flip = flip

        # Set color
        try:
            self.color = np.array(to_rgba(color)) * \
                         np.array([shade, shade, shade, 1])
        except:
            assert False, 'Error! Unable to interpret color %s' % repr(color)

        # Set tranparency
        self.color[3] = alpha
        self.edgecolor=edgecolor

    def draw(self, ax):

        # Draw character
        put_char_in_box(ax, self.c, self.bbox,
                        flip=self.flip,
                        facecolor=self.color,
                        edgecolor=self.edgecolor,
                        font_properties=self.font_properties)



def put_char_in_box(ax, char, bbox, flip=False, facecolor='k',
                    edgecolor='none', 
                    font_properties=None, 
                    zorder=0):

    # Create raw path
    tmp_path = TextPath((0, 0), char, size=1, prop=font_properties)

    # If need to flip character, do it within tmp_path
    if flip:
        transformation = Affine2D().scale(sx=1, sy=-1)
        tmp_path = transformation.transform_path(tmp_path)

    # Get bounding box for temporary character path
    tmp_bbox = tmp_path.get_extents()

    # THIS IS THE KEY TRANSFORMATION
    # 1. Translate character path so that lower left corner is at origin
    # 2. Scale character path to desired width and height
    # 3. Translate character path to desired position
    transformation = Affine2D() \
        .translate(tx=-tmp_bbox.xmin, ty=-tmp_bbox.ymin) \
        .scale(sx=bbox.width / tmp_bbox.width, sy=bbox.height / tmp_bbox.height) \
        .translate(tx=bbox.xmin, ty=bbox.ymin)
    path = transformation.transform_path(tmp_path)

    # Make and display patch
    patch = PathPatch(path, facecolor=facecolor, edgecolor=edgecolor,
                      zorder=zorder)
    ax.add_patch(patch)