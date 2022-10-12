import math
import matplotlib as mpl
import numpy as np
import warnings
from matplotlib.colors import Colormap
from natsort import natsorted
from typing import Mapping

from legendkit import ListLegend


def rotate_points(px, py, origin, angle):
    """
    Rotate points counterclockwise by a given angle around a given origin.

    The angle should be given in degrees.
    """
    angle = math.radians(angle)
    ox, oy = origin

    qx = ox + np.cos(angle) * (px - ox) - np.sin(angle) * (py - oy)
    qy = oy + np.sin(angle) * (px - ox) + np.cos(angle) * (py - oy)
    return qx, qy


def set_default(arg, default):
    if arg is None:
        return default
    else:
        return arg


def get_colormap(name):
    """Handle changes to matplotlib colormap interface in 3.6."""
    try:
        return mpl.colormaps[name]
    except AttributeError:
        return mpl.cm.get_cmap(name)


def register_colormap(name, cmap):
    """Handle changes to matplotlib colormap interface in 3.6."""
    try:
        if name not in mpl.colormaps:
            mpl.colormaps.register(cmap, name=name)
    except AttributeError:
        mpl.cm.register_cmap(name, cmap)


def cat_colors(types, order=None, cmap=None, colors=None):
    if order is None:
        uni_types = np.unique(types)
        uni_types = natsorted(uni_types)
    else:
        uni_types = order
    types_count = len(uni_types)
    uni_mapper = dict(zip(uni_types, np.arange(types_count)))

    if colors is None:
        cmap = set_default(cmap, "echarts")
        if not isinstance(cmap, Colormap):
            cmap = get_colormap(cmap)
        if cmap.N < types_count:
            warnings.warn(f"Usage of duplicated colors, found {types_count} "
                          f"types but only {cmap.N} colors.")
        color_array = [cmap(uni_mapper[t]) for t in types]
        legend_color = [cmap(i) for i in np.arange(types_count)]
    else:
        if isinstance(colors, Mapping):
            color_array = [colors.get(t) for t in types]
            legend_color = [colors.get(t) for t in uni_types]
        else:
            color_array = colors
            cmapper = dict(zip(types, colors))
            legend_color = [cmapper[t] for t in uni_types]

    return color_array, uni_types, legend_color


def set_cat_legend(labels,
                   colors,
                   ax,
                   title=None,
                   shape="circle",
                   edgecolor=None,
                   edgewidth=None,
                   legend_kw=None, ):
    legend_options = dict(
        title=title,
        loc="out right center",
        deviation=0.05,
        handleheight=0.7,
        handlelength=0.7,
        handletextpad=0.5,
        labelspacing=0.3,
        borderpad=0,
        frameon=False
    )
    legend_options = {**legend_options, **legend_kw}
    legend_items = [
        (shape, label, dict(facecolor=color,
                            edgecolor=edgecolor,
                            linewidth=edgewidth,
                            )) for label, color in zip(labels, colors)
    ]
    ListLegend(ax=ax,
               legend_items=legend_items,
               **legend_options)
