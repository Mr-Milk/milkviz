from itertools import cycle
from typing import Union, List, Any

import matplotlib as mpl
import numpy as np
from natsort import natsorted
from matplotlib import cm
from matplotlib import colors as mcolors
from matplotlib.colors import Colormap
from matplotlib.colors import to_hex
from matplotlib.lines import Line2D


Colors = Union[str, List[str], Colormap, List[Colormap]]


def mask_triu(arr, k=1):
    if not isinstance(arr, np.ndarray):
        arr = np.array(arr, dtype=np.float64)
    arr = arr.astype(np.float64)
    shape = arr.shape
    if shape[0] != shape[1]:
        raise ValueError("Must be a square")
    iu = np.triu_indices(shape[0], k=k)
    arr[iu] = np.nan
    return np.fliplr(arr.T)


def norm_arr(arr, size=(1, 100), vmin=None, vmax=None):
    """Normalize the array to a specific range"""
    if not isinstance(arr, np.ndarray):
        arr = np.array(arr)
    arr = arr.flatten()
    add_count = 0
    if vmin is not None:
        arr = np.array([*arr, vmin])
        add_count += 1
    if vmax is not None:
        arr = np.array([*arr, vmax])
        add_count += 1
    amin = np.nanmin(arr)
    amax = np.nanmax(arr)
    size_range = size[1] - size[0]
    arr = (arr - amin) * (size_range / (amax - amin))
    arr += size[0]
    slice_ = -add_count if add_count > 0 else None
    return arr[:slice_]


def adaptive_figsize(size, min_side=5):
    """scale the min number to min_side, while maintain the ratio"""
    size = np.array(size, dtype=np.float64)
    amin = np.amin(size)
    min_ix = np.argmin(size)
    scale = min_side / amin
    if amin < min_side:
        size *= scale
        size[min_ix] = min_side
    return tuple(size)


def set_cbar(ax, patches=None, bbox=None, title=None, cmin=None, cmax=None, ticklabels=None, cmap=None):
    axins = ax.inset_axes(bbox, transform=ax.transAxes)
    fig = ax.get_figure()
    if patches is not None:
        cbar = fig.colorbar(patches, cax=axins)
    else:
        cbar = fig.colorbar(cm.ScalarMappable(cmap=cmap), cax=axins)
    cbar.ax.set_title(title, size=mpl.rcParams["font.size"])
    cbar.ax.yaxis.set_tick_params(length=0)  # hide ticks
    if ticklabels is not None:
        cbar.set_ticks(list(np.linspace(cmin, cmax, num=len(ticklabels))), )
        cbar.ax.set_yticklabels(list(ticklabels))


def set_size_legend(ax, size_arr, markersize_arr, bbox, title):
    legend_items = [Line2D((), (), linestyle="none", marker="o", color="black", markerfacecolor="black",
                           label=f"{round(np.nanmax(size_arr) * ratio, 2)}",
                           markersize=np.sqrt((np.nanmax(markersize_arr))) * ratio
                           ) for ratio in [1.0, 0.66, 0.33]]
    legend = ax.legend(handles=legend_items, loc="upper left", bbox_to_anchor=bbox,
                       frameon=False, labelspacing=1.2, title=title,
                       fontsize=mpl.rcParams["font.size"])
    legend._legend_box.align = "left"
    ax.add_artist(legend)


def set_category_legend(ax, cmapper, bbox, title, marker="o"):
    legend_items = [Line2D((), (), marker=marker, linestyle="none", markersize=8, color=c, markerfacecolor=c, label=t)
                    for t, c in cmapper.items()]
    ncol = round(len(legend_items) / 10)
    ncol = ncol if ncol > 0 else 1
    legend = ax.legend(handles=legend_items, loc="upper left", bbox_to_anchor=bbox,
                       frameon=False, title=title, ncol=ncol, columnspacing=0.8,
                       handletextpad=0.1, fontsize=mpl.rcParams["font.size"])
    ax.add_artist(legend)


def set_spines(ax, status=(0, 0, 0, 0)):
    for spine, s in zip(ax.spines.values(), status):
        spine.set_visible(s)


def set_ticks(ax, xticks="none", yticks="none"):
    ax.xaxis.set_ticks_position(xticks)
    ax.yaxis.set_ticks_position(yticks)
    

def get_cmap_colors(color: Union[str, List[str], Colormap, List[Colormap]]):
    """This utility function allow different color input
    
    1) colormap name, list of colormap name
    2) color name, list of color name
    3) colormap instance, list of instance
    
    """
    if isinstance(color, (str, Colormap)):
        color = [color]
    test_c = color[0]
    if isinstance(test_c, str):
        if mcolors.is_color_like(test_c):
            return [to_hex(c, keep_alpha=True) for c in color]
        else:
            colors = []
            for cmap_ in color:
                cmap = cm.get_cmap(cmap_)
                colors += [to_hex(cmap(i), keep_alpha=True) for i in range(cmap.N)]
            return colors
    else:
        colors = []
        for c in color:
            colors += [to_hex(c(i), keep_alpha=True) for i in range(c.N)]
        return colors




def color_mapper_cat(color: Colors, types: Union[List[Any], np.ndarray]):
    """
    
    Args:
        color: The color array or colormap
        types: All input types

    Returns:
        {type: color}
        
    """
    if len(color) == len(types):
        return dict(zip(types, color))
    else:
        types = natsorted(np.unique(types))
        N = len(types)
        if isinstance(color, str):
            color = [color]

        all_colors = []
        for c in cycle(color):
            if len(all_colors) < N:
                all_colors += get_cmap_colors(c)
            else:
                break

        return dict(zip(types, all_colors))


def color_mapper_val(color: Union[str, Union[str], Colormap], values: Union[List[Any], np.ndarray]):
    if not isinstance(values, np.ndarray):
        values = np.ndarray(values)
    vmin = np.nanmin(values)
    vmax = np.nanmax(values)
    norm = mcolors.Normalize(vmin=vmin, vmax=vmax)
    if not isinstance(color, (str, Colormap)):
        color = ListedColormap(color)
    mapper = cm.ScalarMappable(norm=norm, cmap=color)
    return [to_hex(mapper.to_rgba(v), keep_alpha=True) for v in values]
