from typing import Optional, List, Union, Tuple, Any

import matplotlib as mpl
import matplotlib.axes
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import PatchCollection
from matplotlib.colors import Colormap

from milkviz._dot import set_dot_grid
from milkviz.utils import doc, norm_arr, set_cbar, set_size_legend


@doc
def dot_heatmap(
        dot_size: np.ndarray,
        dot_hue: np.ndarray,
        matrix_hue: Optional[np.ndarray] = None,
        xticklabels: Optional[List[str]] = None,
        yticklabels: Optional[List[str]] = None,
        xlabel: Optional[str] = None,
        ylabel: Optional[str] = None,
        sizes: Tuple[int, int] = (1, 500),
        size_dtype: Any = None,
        dot_cmap: Union[str, Colormap, None] = "RdBu",
        matrix_cmap: Union[str, Colormap, None] = "YlGn",
        size_legend_title: str = "Dot size",
        hue_cbar_title: str = "Dot hue",
        hue_cbar_ticklabels: Optional[List[str]] = None,
        hue_cbar_pos: Optional[Tuple] = None,
        matrix_cbar_title: str = "Matrix",
        matrix_cbar_ticklabels: Optional[List[str]] = None,
        matrix_cbar_pos: Optional[Tuple] = None,
        no_spines: bool = True,
        no_ticks: bool = True,
        ax: Optional[mpl.axes.Axes] = None,
) -> mpl.axes.Axes:
    """Dot heatmap + Matrix heatmap

    Args:
        dot_size: [size]
        dot_hue: [hue]
        matrix_hue: The color array that map to matrix colors
        xticklabels: [xticklabels]
        yticklabels: [yticklabels]
        xlabel: [xlabel]
        ylabel: [ylabel]
        sizes: [sizes]
        size_dtype: [size_dtype]
        dot_cmap: The colormap for dot
        matrix_cmap: The colormap for matrix
        size_legend_title: [size_legend_title]
        hue_cbar_title: [cbar_title] of dot hue
        matrix_cbar_title: [cbar_title] of matrix hue
        hue_cbar_pos: Default is (1.07, 0, 0.1, 0.3)
        matrix_cbar_pos: Default is (1.27, 0, 0.1, 0.3)
        hue_cbar_ticklabels: Text to put on ticks of dot hue colorbar
        matrix_cbar_ticklabels: Text to put on ticks of matrix hue colorbar
        no_spines: [no_spines]
        no_ticks: [no_ticks]
        ax: [ax]

    Returns:
        [return_obj]

    """
    ax, xcoord, ycoord = set_dot_grid(dot_size, ax=ax, xlabel=xlabel, ylabel=ylabel,
                                      xticklabels=xticklabels, yticklabels=yticklabels,
                                      no_spines=no_spines, no_ticks=no_ticks, min_side=3)

    circ_size = norm_arr(dot_size, sizes)
    circ_colors = dot_hue.flatten()
    circ_cmin = np.nanmin(circ_colors)
    circ_cmax = np.nanmax(circ_colors)
    circles = plt.scatter(xcoord, ycoord, s=circ_size, c=circ_colors, cmap=dot_cmap)
    # adding dot size legend
    set_size_legend(ax, dot_size, circ_size, (1.05, 0, 1, 1), size_legend_title, dtype=size_dtype)

    # adding dot colorbar
    hue_cbar_pos = (1.07, 0, 0.1, 0.3) if hue_cbar_pos is None else hue_cbar_pos
    matrix_cbar_pos = (1.27, 0, 0.1, 0.3) if matrix_cbar_pos is None else matrix_cbar_pos
    set_cbar(ax, circles, hue_cbar_pos, hue_cbar_title, circ_cmin, circ_cmax, hue_cbar_ticklabels)

    if matrix_hue is not None:
        rects = [mpatches.Rectangle((rx - 0.5, ry - 0.5), 1, 1) for rx, ry in zip(xcoord, ycoord)]
        rects_colors = matrix_hue.flatten()
        rects_cmin = np.nanmin(rects_colors)
        rects_cmax = np.nanmax(rects_colors)
        rects = PatchCollection(rects, array=rects_colors, cmap=matrix_cmap)
        rects.set_clim(rects_cmin, rects_cmax)
        rects.set_zorder(-1)
        ax.add_collection(rects)

        set_cbar(ax, rects, matrix_cbar_pos, matrix_cbar_title, rects_cmin, rects_cmax, matrix_cbar_ticklabels)
    plt.tight_layout()
    return ax
