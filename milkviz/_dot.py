from typing import Optional, List, Union, Tuple, Any

import matplotlib as mpl
import matplotlib.axes
import matplotlib.pyplot as plt
import numpy as np

from milkviz.types import Pos
from milkviz.utils import norm_arr, doc, set_size_legend, set_spines, set_ticks


def set_dot_grid(data,
                 ax=None,
                 xlabel=None,
                 ylabel=None,
                 xticklabels=None,
                 yticklabels=None,
                 no_spines=True,
                 no_ticks=True,
                 min_side=5,
                 ):
    Y, X = data.shape
    x, y = np.meshgrid(np.arange(X), np.arange(Y))  # Get the coordinates
    xcoord = x.flatten()
    ycoord = y.flatten()

    if ax is None:
        figsize = (0.3 * X + 2, 0.3 * Y + 1)
        print(figsize)
        _, ax = plt.subplots(figsize=figsize)
    if no_spines:
        set_spines(ax)
    if no_ticks:
        set_ticks(ax)
    ax.set_aspect("equal")
    ax.set_xlim(-0.5, X - 0.5)
    ax.set_ylim(-0.5, Y - 0.5)
    ax.set(
        xlabel=xlabel,
        ylabel=ylabel,
        xticks=np.arange(X),
        yticks=np.arange(Y),
        xticklabels=xticklabels if xticklabels is not None else [],
        yticklabels=yticklabels if yticklabels is not None else [],
    )
    plt.xticks(rotation=90)

    return ax, xcoord, ycoord


@doc
def dot(
        dot_size: np.ndarray,
        dot_hue: Union[str, np.ndarray, None] = None,
        xticklabels: Optional[List[str]] = None,
        yticklabels: Optional[List[str]] = None,
        xlabel: Optional[str] = None,
        ylabel: Optional[str] = None,
        sizes: Tuple[int, int] = (10, 250),
        dtype: Any = None,
        legend_title: Optional[str] = None,
        legend_pos: Pos = None,
        no_spines: bool = True,
        no_ticks: bool = True,
        ax: Optional[mpl.axes.Axes] = None,
) -> mpl.axes.Axes:
    """Dot plot

    Args:
        dot_size: [size]
        dot_hue: [hue]
        xticklabels: [xticklabels]
        yticklabels: [yticklabels]
        xlabel: [xlabel]
        ylabel: [ylabel]
        sizes: [sizes]
        dtype: [dtype]
        legend_title: [legend_title]
        legend_pos: [legend_pos]
        no_spines: [no_spines]
        no_ticks: [no_ticks]
        ax: [ax]

    Returns:
        [return_obj]

    """

    ax, xcoord, ycoord = set_dot_grid(dot_size, ax=ax, xlabel=xlabel, ylabel=ylabel,
                                      xticklabels=xticklabels, yticklabels=yticklabels,
                                      no_spines=no_spines, no_ticks=no_ticks, min_side=3)

    if dot_hue is not None:
        if isinstance(dot_hue, str):
            circ_colors = np.repeat(dot_hue, dot_size.size)
        else:
            if np.array((dot_hue.shape == dot_size.shape)).all():
                circ_colors = dot_hue.flatten()
            else:
                raise ValueError("dot_hue does not match the shape of dot_size")
    else:
        circ_colors = np.repeat("#D75455", dot_size.size)

    circ_size = norm_arr(dot_size, sizes)
    _ = plt.scatter(xcoord, ycoord, s=circ_size, c=circ_colors)
    # adding dot size legend
    set_size_legend(ax, dot_size, circ_size, pos=legend_pos, title=legend_title, dtype=dtype)
    ax.grid(False)
    return ax
