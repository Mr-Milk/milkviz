from typing import Optional, List, Union, Tuple

import matplotlib as mpl
import matplotlib.axes
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import Colormap

from milkviz.utils import norm_arr, doc
from milkviz.utils.fig import set_size_legend, set_cbar


@doc
def bubble(data: Optional[pd.DataFrame] = None,
           x: Union[str, np.ndarray, None] = None,
           y: Union[str, np.ndarray, None] = None,
           hue: Union[str, np.ndarray, None] = None,
           size: Union[str, np.ndarray, None] = None,
           cmap: Union[str, Colormap] = "RdBu",
           sizes: Tuple[int, int] = (1, 500),
           size_legend_title: str = "size",
           hue_cbar_title: str = "hue",
           hue_cbar_ticklabels: Optional[List[str]] = None,
           ax: Optional[mpl.axes.Axes] = None,
           ) -> mpl.axes.Axes:
    """Bubble plot

    Args:
        data: [data]
        x: [x]
        y: [y]
        hue: [hue]
        size: [size]
        cmap: [cmap]
        sizes: [sizes]
        size_legend_title: [size_legend_title]
        hue_cbar_title: [cbar_title]
        hue_cbar_ticklabels: Overwrite the ticklabels on colorbar
        ax: [ax]

    Returns:
        [return_obj]

    """
    if data is not None:
        x = data[x].to_numpy()
        y = data[y].to_numpy()
        hue = data[hue].to_numpy() if hue is not None else None
        size = data[size].to_numpy() if size is not None else None

    if size is None:
        raise ValueError("size must be provided")

    if ax is None:
        ax = plt.gca()

    circ_size = norm_arr(size, sizes)
    bubbles = plt.scatter(x, y, s=circ_size, c=hue, cmap=cmap)
    set_size_legend(ax, size, circ_size, bbox=(1.05, 0, 1, 1), title=size_legend_title)
    if hue is not None:
        cmin = np.nanmin(hue)
        cmax = np.nanmax(hue)
        set_cbar(ax, bubbles, (1.07, 0, 0.1, 0.3), hue_cbar_title, cmin, cmax, hue_cbar_ticklabels)

    return ax
