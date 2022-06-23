from __future__ import annotations

from typing import Optional, List, Tuple, Any, Dict

import matplotlib as mpl
import matplotlib.axes
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from legendkit import SizeLegend, Colorbar
from milkviz.utils import norm_arr, doc, set_default, set_spines


@doc
def bubble(data: Optional[pd.DataFrame] = None,
           x: str | List | np.ndarray = None,
           y: str | List | np.ndarray = None,
           hue: str | List | np.ndarray = None,
           size: str | List | np.ndarray = None,
           cmap: Any = None,
           sizes: Tuple[int, int] = (10, 250),
           dtype: Any = None,
           legend_kw: Dict = None,
           cbar_kw: Dict = None,
           ax: mpl.axes.Axes = None,
           ) -> mpl.axes.Axes:
    """Bubble plot

    Args:
        data: [data]
        x: [x]
        y: [y]
        hue: [hue]
        size: [size]
        cmap: [cmap], default to "RdBu"
        sizes: [sizes]
        dtype: [dtype]
        legend_kw: The options to configure legend
        cbar_kw: The options to configure colorbar
        ax: [ax]

    Returns:
        [return_obj]

    """
    cmap = set_default(cmap, "RdBu")
    ax = set_default(ax, plt.gca())
    legend_kw = set_default(legend_kw, {})
    cbar_kw = set_default(cbar_kw, {})

    if data is not None:
        x = data[x].to_numpy()
        y = data[y].to_numpy()
        hue = data[hue].to_numpy() if hue is not None else None
        size = data[size].to_numpy() if size is not None else None

    if size is None:
        raise ValueError("At least `size` must be provided")

    circ_size = norm_arr(size, sizes)
    bubbles = ax.scatter(x, y, s=circ_size, c=hue, cmap=cmap)

    legend_options = dict(
        bbox_to_anchor=(1.05, 1),
        bbox_transform=ax.transAxes,
        loc="upper left",
        title_align="left",
        dtype=dtype
    )
    legend_options = {**legend_options, **legend_kw}
    SizeLegend(circ_size, array=size, ax=ax, **legend_options)

    if hue is not None:
        cbar_options = dict(
            bbox_to_anchor=(1.05, 0),
            bbox_transform=ax.transAxes,
            loc="lower left",
            title_align="left",
        )
        cbar_options = {**cbar_options, **cbar_kw}
        Colorbar(bubbles, ax=ax, **cbar_options)
    set_spines(ax, (1, 0, 1, 0))

    return ax
