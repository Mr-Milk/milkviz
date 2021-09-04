from itertools import cycle
from typing import Union, List, Any

import matplotlib as mpl
from matplotlib import colors as mcolors
from matplotlib import cm
import numpy as np
from matplotlib.lines import Line2D


def norm_arr(arr, size=(1, 100)):
    """Normalize the array to a specific range"""
    if not isinstance(arr, np.ndarray):
        arr = np.array(arr)
    arr = arr.flatten()
    amin = np.nanmin(arr)
    amax = np.nanmax(arr)
    size_range = size[1] - size[0]
    arr = (arr - amin) * (size_range / (amax - amin))
    arr += size[0]
    return arr


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


def set_cbar(ax, patches, bbox, title, cmin, cmax, ticklabels=None):
    axins = ax.inset_axes(bbox, transform=ax.transAxes)
    fig = ax.get_figure()
    cbar = fig.colorbar(patches, cax=axins)
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
    legend_items = [Line2D((), (), marker=marker, linestyle="none", markersize=5, color=c, markerfacecolor=c, label=t)
                    for t, c in cmapper.items()]

    legend = ax.legend(handles=legend_items, loc="upper left", bbox_to_anchor=bbox,
                       frameon=False, title=title, ncol=round(len(legend_items) / 10),
                       fontsize=mpl.rcParams["font.size"])
    ax.add_artist(legend)


def set_spines(ax, status=(0, 0, 0, 0)):
    for spine, s in zip(ax.spines.values(), status):
        spine.set_visible(s)


def set_ticks(ax, xticks="none", yticks="none"):
    ax.xaxis.set_ticks_position(xticks)
    ax.yaxis.set_ticks_position(yticks)


def color_mapper_cat(color: Union[str, List[str]], types: Union[List[Any], np.ndarray]):
    N = len(types)
    if isinstance(color, str):
        color = [color]

    all_colors = []
    for c in cycle(color):
        if len(all_colors) < N:
            cmap = cm.get_cmap(c)
            all_colors += [cmap(i) for i in range(cmap.N)]
        else:
            break

    return dict(zip(types, all_colors))


def color_mapper_val(color: str, values: Union[List[Any], np.ndarray]):
    if not isinstance(values, np.ndarray):
        values = np.ndarray(values)
    vmin = np.nanmin(values)
    vmax = np.nanmax(values)
    norm = mcolors.Normalize(vmin=vmin, vmax=vmax)
    mapper = cm.ScalarMappable(norm=norm, cmap=color)
    return [mapper.to_rgba(v) for v in values]
