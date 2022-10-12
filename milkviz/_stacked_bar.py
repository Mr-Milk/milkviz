from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from itertools import tee
from matplotlib.axes import Axes
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle
from natsort import natsorted
from typing import Callable

from .utils import set_default, cat_colors, set_cat_legend


def stacked_bar(data,
                group=None,
                value=None,
                stacked=None,
                *,
                orient="v",
                group_order=None,
                stacked_order=None,
                percentage=False,
                barwidth=.8,
                cmap=None,
                colors=None,
                show_values=False,
                props=None,
                legend_kw=None,
                ax=None,
                ) -> Axes:
    """Stacked bar plot

    Parameters
    ----------
    data : pd.DataFrame
        The data used to plot
    group : str
        The column used to group
    value : str
        The column that contains numeric values for plotting
    stacked : str
        The column to plot as stack
    orient : "v" or "h"
        The orientation of the plot
    group_order :
    stacked_order :
    percentage : bool
        Normalize stack to 1, ensure all stacks have same height
    cmap :
    colors : array, mapping
        Either array that represents colors or a dict that map types to colors
    barwidth : float
        The width of stacked bar, should be in (0, 1)
    show_values : bool
        Whether to display values of each block,
        or you can pass in a function to tell when to display
        like `lambda x: x > 100` will only display when value exceed 100
    props : dict
        Use to style text, pass to :func:`matplotlib.axes.Axes.text`
    legend_kw : dict
        The options to configure legend
    ax :

    Returns
    -------
    Axes

    """

    cmap = set_default(cmap, "echarts")
    legend_kw = set_default(legend_kw, {})
    props = set_default(props, {})

    def show_values_func(va):
        return va
    if isinstance(show_values, Callable):
        show_values_func = show_values
        show_values = True

    if ax is None:
        ax = plt.gca()

    if stacked_order is None:
        stacked_order = natsorted(data[stacked].unique())
    if group_order is None:
        group_order = natsorted(data[group].unique())

    _, legend_labels, legend_colors = \
        cat_colors(stacked_order, stacked_order, cmap, colors)

    start_x = 1
    gb = data.groupby([group], sort=False)
    rects = []
    lims = []

    textprops = dict(ha="center", va="center",
                     bbox=dict(fc="white", alpha=0.7))
    textprops = {**textprops, **props}

    mapping = {key: i for i, key in enumerate(stacked_order[::-1])}

    for s in group_order:
        df = gb.get_group(s).set_index(stacked)
        slice_ix = sorted(df.index, key=lambda d: mapping[d])
        df = df.loc[slice_ix]
        text = df[value].to_numpy()
        v_sum = np.sum(text)
        vs = np.cumsum(text)
        if percentage:
            vs = vs / v_sum
        lims.append(np.max(vs))
        x = start_x - barwidth / 2
        for v, c, t in zip(vs[::-1], legend_colors, text[::-1]):
            if orient == "v":
                rects.append(
                    Rectangle(xy=(x, 0), width=barwidth, height=v,
                              facecolor=c)
                )
                if show_values:
                    ax.text(start_x, v, t, **textprops)
            else:
                rects.append(
                    Rectangle(xy=(0, x), height=barwidth, width=v,
                              facecolor=c)
                )
                if show_values:
                    ax.text(v, start_x, t, rotation=-90, **textprops)

        start_x += 1
    patches = PatchCollection(rects, match_original=True)
    ax.add_collection(patches)

    value_label = "Percentage (%)" if percentage else value
    if orient == "v":
        ax.set_xlim(0.5, len(group_order) + 0.5)
        ax.set_ylim(0, np.max(lims) * 1.05)
        ax.xaxis.set_ticks(
            ticks=np.arange(1, len(group_order)+1),
            labels=group_order,
        )
        ax.set(xlabel=group, ylabel=value_label)
    else:
        ax.set_ylim(0.5, len(group_order) + 0.5)
        ax.set_xlim(0, np.max(lims) * 1.05)
        ax.yaxis.set_ticks(
            ticks=np.arange(1, len(group_order) + 1),
            labels=group_order,
        )
        ax.set(xlabel=value_label, ylabel=group)

    set_cat_legend(
        labels=legend_labels,
        colors=legend_colors,
        ax=ax,
        title=stacked,
        shape="square",
        legend_kw=legend_kw,
    )
    return ax
