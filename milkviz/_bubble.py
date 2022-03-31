from typing import Optional, List, Tuple, Any

import matplotlib as mpl
import matplotlib.axes
import matplotlib.pyplot as plt
import pandas as pd

from milkviz.types import OneDimAny, Colors, Pos, Text, Size
from milkviz.utils import norm_arr, doc, set_default
from milkviz.utils import set_size_legend, set_cbar


@doc
def bubble(data: Optional[pd.DataFrame] = None,
           x: OneDimAny = None,
           y: OneDimAny = None,
           hue: OneDimAny = None,
           size: OneDimAny = None,
           cmap: Colors = None,
           sizes: Tuple[int, int] = (10, 250),
           legend_title: Optional[str] = None,
           legend_pos: Pos = None,
           dtype: Any = None,
           cbar_title: Text = None,
           cbar_ticklabels: Optional[List[str]] = None,
           cbar_pos: Pos = None,
           cbar_size: Size = None,
           ax: Optional[mpl.axes.Axes] = None,
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
        legend_title: [size_legend_title]
        legend_pos: [legend_pos]
        dtype: [dtype]
        cbar_title: [cbar_title]
        cbar_ticklabels: Overwrite the ticklabels on colorbar
        cbar_pos: [cbar_pos]
        cbar_size: [cbar_size]
        ax: [ax]

    Returns:
        [return_obj]

    """
    cmap = set_default(cmap, "RdBu")
    ax = set_default(ax, plt.gca())

    if data is not None:
        x = data[x].to_numpy()
        y = data[y].to_numpy()
        hue = data[hue].to_numpy() if hue is not None else None
        size = data[size].to_numpy() if size is not None else None

    if size is None:
        raise ValueError("At least `size` must be provided")

    circ_size = norm_arr(size, sizes)
    bubbles = ax.scatter(x, y, s=circ_size, c=hue, cmap=cmap)

    set_size_legend(ax, size, circ_size, pos=legend_pos, title=legend_title, dtype=dtype)
    if hue is not None:
        set_cbar(ax,
                 patches=bubbles,
                 bbox=cbar_pos,
                 size=cbar_size,
                 title=cbar_title,
                 c_array=hue,
                 ticklabels=cbar_ticklabels)

    return ax
