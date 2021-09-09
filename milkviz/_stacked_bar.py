from typing import Optional, List, Union, Tuple

import matplotlib as mpl
from matplotlib.axes import Axes
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import Colormap
import seaborn as sns

from milkviz.utils import norm_arr, doc
from milkviz.utils import set_size_legend, set_cbar, get_cmap_colors, set_category_legend, set_spines


def fold_add(arr):
    new_arr = np.zeros(arr.size)
    new_arr[0] = arr[0]
    for i in range(arr.size - 1):
        new_arr[i + 1] = arr[:i + 2].sum()
    return new_arr


@doc
def stacked_bar(data: Optional[pd.DataFrame] = None,
                x: Union[str, np.ndarray, None] = None,
                y: Union[str, np.ndarray, None] = None,
                stacked: Union[str, np.ndarray, None] = None,
                orientation: str = "vertical",
                percentage: bool = False,
                color: Union[str, Colormap] = "tab20",
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
        orientation: "vertical" or "horizontal"
        percentage: Normalize value to 1
        color: [color]
        ax: [ax]
        **kwargs: Pass to `seaborn.barplot <https://seaborn.pydata.org/generated/seaborn.barplot.html#seaborn.barplot>`_

    Returns:
        [return_obj]

    """

    if ax is None:
        _, ax = plt.subplots()

    if data is None:
        data = pd.DataFrame({"x": x, "y": y, "stacked": stacked})
        x = "x"
        y = "y"
        stacked = "stacked"

    value_key, label_key = (y, x) if orientation == "vertical" else (x, y)
    stacked_order = data[stacked].unique()
    label_order = data[label_key].unique()

    all_g = []
    for label in label_order:
        g = data[data[label_key] == label].set_index(stacked)
        g = g.loc[stacked_order, :]
        v = g[value_key].to_numpy()
        if percentage:
            v = v / v.sum()
        g[value_key] = fold_add(v)
        all_g.append(g)
    # This reverse step is to make the label column in the right order
    data_g = pd.concat(all_g[::-1]).reset_index()

    colors = get_cmap_colors(color)
    # This reverse step is to make the stacked column in the right order
    legends_cmapper = {}
    for (n, g), c in zip(data_g.iloc[::-1, :].groupby(stacked, sort=False), colors):
        bar = sns.barplot(x=x, y=y, data=g, ax=ax, color=c, **kwargs)
        if show_values:
            for i in range(len(g)):
                text = g.iloc[i,:][value_key]
                if orientation == "vertical":
                    bar.text(i, text, text, ha="center", va="center", bbox=dict(fc="white", alpha=0.7))
                else:
                    bar.text(text, i, text, ha="center", va="center", rotation=-90, bbox=dict(fc="white", alpha=0.7))
        legends_cmapper[n] = c
    set_category_legend(ax, legends_cmapper, (1.07, 0, 0.1, 0.3), title=stacked, marker="s")
    set_spines(ax, (1, 0, 1, 0))
    return ax
