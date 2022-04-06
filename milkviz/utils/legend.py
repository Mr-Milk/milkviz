import matplotlib as mpl
import numpy as np
from matplotlib import cm
from matplotlib.axes import Axes
from matplotlib.collections import CircleCollection
from matplotlib.colors import Normalize
from matplotlib.lines import Line2D
from matplotlib.patches import Ellipse, Patch

from .params import set_default

CBAR_W, CBAR_H = (0.5, 1.5)
CIRCLE_CBAR_W, CIRCLE_CBAR_H = (0.8, 1.5)


def get_fraction_side(ax, actual_size):
    fig_w, fig_h = ax.get_figure().get_size_inches()
    return actual_size[0] / fig_w, actual_size[1] / fig_h


def parse_label(label, dtype=None):
    if dtype is None:
        dtype = type(label)
    if isinstance(label, str):
        return label
    elif (dtype == int) | np.issubdtype(dtype, np.integer):
        return int(label)
    elif (dtype == float) | np.issubdtype(dtype, np.floating):
        return round(label, 1)
    else:
        return label


def set_cbar(ax: Axes,
             patches=None,
             c_array=None,
             bbox=None,
             size=None,
             title=None,
             ticklabels=None,
             cmap=None,
             cmin=None,
             cmax=None,
             dtype=None,
             ):
    """Create a colorbar on the current Axes

    Args:
        ax:
        patches:
        bbox: default to (1.05, 0, ?, ?)
        title:
        c_array:
        ticklabels:
        cmap:
        size:

    Returns:

    """
    bbox = set_default(bbox, (1.05, 0, 0.1, 0.2))
    size = set_default(size, (CBAR_W, CBAR_H))
    frac_w, frac_h = get_fraction_side(ax, size)
    bbox = (bbox[0], bbox[1], frac_w, frac_h)
    axins = ax.inset_axes(bbox, transform=ax.transAxes)
    fig = ax.get_figure()

    if (cmin is None) & (cmax is None):
        if c_array is not None:
            cmin = np.nanmin(c_array)
            cmax = np.nanmax(c_array)
            if dtype is None:
                dtype = type(c_array.flatten()[0])
        else:
            raise ValueError("Either supply `cmin` and `cmax` or `c_array`.")
    else:
        if dtype is None:
            dtype = type(cmin)
    if patches is not None:
        cbar = fig.colorbar(patches, cax=axins)
    else:
        cbar = fig.colorbar(cm.ScalarMappable(norm=Normalize(vmin=cmin, vmax=cmax), cmap=cmap), cax=axins)
    cbar.ax.set_title(title, size=mpl.rcParams["font.size"])
    cbar.ax.yaxis.set_tick_params(direction="in", color="white", width=1)  # Inward ticks and in white color
    cbar.outline.set_visible(0)  # turn off outlines

    if ticklabels is not None:
        cbar.set_ticks(list(np.linspace(cmin, cmax, num=len(ticklabels))), )
        cbar.ax.set_yticklabels(list(ticklabels))
    else:
        labels = list(np.linspace(cmin, cmax, num=4))
        cbar.set_ticks(labels)
        labels = [parse_label(label, dtype=dtype) for label in labels]
        cbar.ax.set_yticklabels(labels)


def set_circle_cbar(ax,
                    c_array=None,
                    bbox=None,
                    size=None,
                    title=None,
                    ticklabels=None,
                    cmap=None,
                    ):
    bbox = set_default(bbox, (1.05, 0.5, 0.1, 0.2))
    size = set_default(size, (CIRCLE_CBAR_W, CIRCLE_CBAR_H))
    frac_w, frac_h = get_fraction_side(ax, size)
    bbox = (bbox[0], bbox[1], frac_w, frac_h)

    axins = ax.inset_axes(bbox, transform=ax.transAxes)
    patch = Ellipse((0.35, 0.5), 0.7, 1, facecolor='none')
    axins.add_patch(patch)
    axins.imshow(np.repeat(np.linspace(0, 1, num=100), 100).reshape(100, 100),
                 interpolation='none',
                 cmap=cmap,
                 origin='lower',
                 extent=[0, 1, 0, 1],
                 clip_path=patch,
                 clip_on=True)
    axins.set_axis_off()
    axins.set_title(title, size=mpl.rcParams["font.size"])

    if ticklabels is not None:
        lower_label = ticklabels[0]
        upper_label = ticklabels[-1]
    elif c_array is not None:
        lower_label = np.nanmin(c_array)
        upper_label = np.nanmax(c_array)
    else:
        lower_label = None
        upper_label = None
    upper_label = parse_label(upper_label)
    lower_label = parse_label(lower_label)
    axins.text(x=0.7, y=1, s=upper_label, ha="left", va="top")
    axins.text(x=0.7, y=0, s=lower_label, ha="left", va="bottom")


SHARE_LEGEND_OPTIONS = dict(
    loc="upper left",
    frameon=False,
    borderpad=0,
    borderaxespad=0,
    fontsize=mpl.rcParams["font.size"]
)


def set_size_legend(ax,
                    size_arr,
                    markersize_arr,
                    pos=None,
                    title=None,
                    dtype=None):
    pos = set_default(pos, (1.05, 0))
    if dtype is None:
        dtype = type(size_arr.flatten()[0])
    bbox = (*pos, 1, 1)
    size_arr = np.asarray(size_arr, dtype=dtype).flatten()
    legend_items = []
    m_min = np.nanmin(markersize_arr)
    m_max = np.nanmax(markersize_arr)
    marker_incr = m_max - m_min

    s_min = np.nanmin(size_arr)
    s_max = np.nanmax(size_arr)
    size_incr = s_max - s_min

    for ratio, text in zip([1.0, 0.8, 0.6, 0.4, 0.2], ["100%", "80%", "60%", "40%", "20%"]):
        label = parse_label(s_min + size_incr * ratio, dtype=dtype)
        item = CircleCollection([m_min + marker_incr * ratio], label=f"{label} - {text}", facecolors="#1C1C1C")
        legend_items.append(item)
    legend = ax.legend(handles=legend_items,
                       bbox_to_anchor=bbox,
                       labelspacing=1.2,
                       title=title,
                       **SHARE_LEGEND_OPTIONS
                       )
    legend._legend_box.align = "left"
    ax.add_artist(legend)


MARKER_SIZE = {"o": 8, "s": 12}


def set_category_legend(ax, cmapper, bbox, title, ncol=None, marker="o", markersize=None, reverse=False):
    if markersize is None:
        markersize = MARKER_SIZE[marker]
    legend_items = [
        Line2D((), (), marker=marker, linestyle="none", markersize=markersize, color=c, markerfacecolor=c, label=t)
        for t, c in cmapper.items()]
    if reverse:
        legend_items = legend_items[::-1]
    if ncol is None:
        ncol = int(len(legend_items) / 6)
        ncol = ncol if ncol > 0 else 1
    legend = ax.legend(handles=legend_items,
                       bbox_to_anchor=bbox,
                       title=title,
                       ncol=ncol,
                       columnspacing=0.8,
                       handletextpad=0.1,
                       **SHARE_LEGEND_OPTIONS,
                       )
    if ncol == 1:
        legend._legend_box.align = "left"
    ax.add_artist(legend)
    return ncol


def set_category_circle_legend(ax,
                               cmapper,
                               pos,
                               title=None,
                               ncol=None,
                               reverse=False,
                               markersize=None,
                               ):
    markersize = set_default(markersize, 8)
    legend_items = [CircleCollection([markersize ** 2], label=t, facecolors=c) for t, c in cmapper.items()]
    if reverse:
        legend_items = legend_items[::-1]
    if ncol is None:
        ncol = int(len(legend_items) / 6)
        ncol = ncol if ncol > 0 else 1
    legend = ax.legend(handles=legend_items,
                       handlelength=1,
                       handleheight=1,
                       bbox_to_anchor=(*pos, 1, 1),
                       title=title,
                       ncol=ncol,
                       columnspacing=0.8,
                       handletextpad=0.5,
                       **SHARE_LEGEND_OPTIONS)
    if ncol == 1:
        legend._legend_box.align = "left"
    ax.add_artist(legend)
    return ncol


def set_category_square_legend(ax,
                               cmapper,
                               pos=None,
                               title=None,
                               ncol=None,
                               reverse=False):
    pos = set_default(pos, (1.05, 0))
    legend_items = [Patch(color=c, label=t) for t, c in cmapper.items()]
    if reverse:
        legend_items = legend_items[::-1]
    if ncol is None:
        ncol = int(len(legend_items) / 6)
        ncol = ncol if ncol > 0 else 1
    legend = ax.legend(handles=legend_items,
                       handlelength=1.2,
                       handleheight=1.5,
                       bbox_to_anchor=(*pos, 1, 1),
                       title=title,
                       ncol=ncol,
                       labelspacing=0.25,
                       handletextpad=0.4,
                       **SHARE_LEGEND_OPTIONS)
    if ncol == 1:
        legend._legend_box.align = "left"
    ax.add_artist(legend)
    return ncol
