from typing import Optional, Union

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.axes import Axes
from matplotlib.colors import Colormap

from milkviz.utils import doc
from milkviz.utils import get_cmap_colors, set_category_legend, set_spines


def fold_add(arr):
    new_arr = np.zeros(arr.size)
    new_arr[0] = arr[0]
    for i in range(arr.size - 1):
        new_arr[i + 1] = arr[:i + 2].sum()
    return new_arr.astype(arr.dtype)  # preserve the data type


@doc
def stacked_bar(data: Optional[pd.DataFrame] = None,
                x: Union[str, np.ndarray, None] = None,
                y: Union[str, np.ndarray, None] = None,
                stacked: Union[str, np.ndarray, None] = None,
                orient: str = "v",
                percentage: bool = False,
                cmap: Union[str, Colormap] = "tab20",
                show_values: bool = False,
                ax: Optional[mpl.axes.Axes] = None,
                **kwargs,
                ) -> Axes:
    """Stacked bar plot

    Args:
        data: [data]
        x: [x]
        y: [y]
        stacked: Which columns to plot as stacked type
        orient: "v" or "h"
        percentage: Normalize value to 1
        cmap: [cmap]
        show_values: Whether to display values of each block
        ax: [ax]
        **kwargs: Pass to `seaborn.barplot <https://seaborn.pydata.org/generated/seaborn.barplot.html#seaborn.barplot>`_

    Returns:
        [return_obj]

    """

    if ax is None:
        ax = plt.gca()

    if data is None:
        data = pd.DataFrame({"x": x, "y": y, "stacked": stacked})
        x = "x"
        y = "y"
        stacked = "stacked"

    value_key, label_key = (y, x) if orient == "v" else (x, y)
    stacked_order = data[stacked].unique()
    label_order = data[label_key].unique()

    all_g = []
    for label in label_order:
        g = data[data[label_key] == label].set_index(stacked)
        s_order = []
        for i in stacked_order:
            if i in g.index:
                s_order.append(i)
        g = g.loc[s_order, :]
        v = g[value_key].to_numpy()
        if percentage:
            v = v / v.sum()
        g[value_key] = fold_add(v)
        all_g.append(g)
    # This reverse step is to make the label column in the right order
    data_g = pd.concat(all_g[::-1]).reset_index()

    colors = get_cmap_colors(cmap)
    # This reverse step is to make the stacked column in the right order
    legends_cmapper = {}
    for (n, g), c in zip(data_g.iloc[::-1, :].groupby(stacked, sort=False), colors):
        bar = sns.barplot(x=x, y=y, data=g, ax=ax, color=c, orient=orient, ci=None, **kwargs)
        if show_values:
            for i in range(len(g)):
                text = g.iloc[i, :][value_key]
                if orient == "v":
                    bar.text(i, text, text, ha="center", va="center", bbox=dict(fc="white", alpha=0.7))
                else:
                    bar.text(text, i, text, ha="center", va="center", rotation=-90, bbox=dict(fc="white", alpha=0.7))
        legends_cmapper[n] = c
    set_category_legend(ax, legends_cmapper, (1.05, 0, 1, 1), title=stacked, marker="s")
    set_spines(ax, (1, 0, 1, 0))
    return ax
