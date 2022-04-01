from typing import Optional, List, Union, Tuple, Any

import matplotlib as mpl
import matplotlib.axes
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import PatchCollection
from matplotlib.colors import Colormap

from milkviz._dot import set_dot_grid
from milkviz.types import Pos, Size
from milkviz.utils import doc, norm_arr, set_cbar, set_size_legend, set_circle_cbar, set_default


@doc
def dot_heatmap(
        dot_size: np.ndarray,
        dot_hue: np.ndarray,
        matrix_hue: Optional[np.ndarray] = None,
        xticklabels: Optional[List[str]] = None,
        yticklabels: Optional[List[str]] = None,
        xlabel: Optional[str] = None,
        ylabel: Optional[str] = None,
        sizes: Tuple[int, int] = (10, 250),
        dtype: Any = None,
        dot_cmap: Union[str, Colormap, None] = None,
        matrix_cmap: Union[str, Colormap, None] = None,
        legend_title: Optional[str] = None,
        legend_pos: Pos = None,
        hue_cbar_title: Optional[str] = None,
        hue_cbar_ticklabels: Optional[List[str]] = None,
        hue_cbar_pos: Pos = None,
        hue_cbar_size: Size = None,
        matrix_cbar_title: Optional[str] = None,
        matrix_cbar_ticklabels: Optional[List[str]] = None,
        matrix_cbar_pos: Optional[Tuple] = None,
        matrix_cbar_size: Size = None,
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
        dtype: [dtype]
        dot_cmap: The colormap for dot, default: "RdBu"
        matrix_cmap: The colormap for matrix, default: "YlGn"
        legend_title: [legend_title]
        legend_pos: [legend_pos]
        hue_cbar_title: [cbar_title] of dot hue
        matrix_cbar_title: [cbar_title] of matrix hue
        hue_cbar_pos: Default is (1.07, 0, 0.1, 0.3)
        matrix_cbar_pos: Default is (1.27, 0, 0.1, 0.3)
        hue_cbar_ticklabels: Text to put on ticks of dot hue colorbar, notice that it can only display two labels
        matrix_cbar_ticklabels: Text to put on ticks of matrix hue colorbar
        hue_cbar_size: [cbar_size]
        matrix_cbar_size: [cbar_size]
        no_spines: [no_spines]
        no_ticks: [no_ticks]
        ax: [ax]

    Returns:
        [return_obj]

    """
    dot_cmap = set_default(dot_cmap, "RdBu")
    matrix_cmap = set_default(matrix_cmap, "YlGn")
    ax, xcoord, ycoord = set_dot_grid(dot_size, ax=ax, xlabel=xlabel, ylabel=ylabel,
                                      xticklabels=xticklabels, yticklabels=yticklabels,
                                      no_spines=no_spines, no_ticks=no_ticks)

    circ_size = norm_arr(dot_size, sizes)
    circ_colors = dot_hue.flatten()
    circles = plt.scatter(xcoord, ycoord, s=circ_size, c=circ_colors, cmap=dot_cmap)
    # adding dot size legend
    set_size_legend(ax, dot_size, circ_size, pos=legend_pos, title=legend_title, dtype=dtype)

    # adding dot colorbar
    if (hue_cbar_pos is None) & (matrix_hue is None):
        hue_cbar_pos = (1.05, 0)
    elif hue_cbar_pos is None:
        hue_cbar_pos = (1.05, 0.4)
    matrix_cbar_pos = (1.05, 0) if matrix_cbar_pos is None else matrix_cbar_pos
    if matrix_hue is None:
        set_cbar(ax,
                 patches=circles,
                 c_array=circ_colors,
                 bbox=hue_cbar_pos,
                 size=hue_cbar_size,
                 title=hue_cbar_title,
                 ticklabels=hue_cbar_ticklabels,
                 cmap=dot_cmap)
    else:
        set_circle_cbar(ax,
                        c_array=circ_colors,
                        bbox=hue_cbar_pos, size=hue_cbar_size,
                        title=hue_cbar_title,
                        ticklabels=hue_cbar_ticklabels,
                        cmap=dot_cmap)

    if matrix_hue is not None:
        rects = [mpatches.Rectangle((rx - 0.5, ry - 0.5), 1, 1) for rx, ry in zip(xcoord, ycoord)]
        rects_colors = matrix_hue.flatten()
        rects_cmin = np.nanmin(rects_colors)
        rects_cmax = np.nanmax(rects_colors)
        rects = PatchCollection(rects, array=rects_colors, cmap=matrix_cmap)
        rects.set_clim(rects_cmin, rects_cmax)
        rects.set_zorder(-1)
        ax.add_collection(rects)

        set_cbar(ax,
                 patches=rects,
                 c_array=rects_colors,
                 bbox=matrix_cbar_pos,
                 size=matrix_cbar_size,
                 title=matrix_cbar_title,
                 ticklabels=matrix_cbar_ticklabels,
                 cmap=matrix_cmap
                 )
    plt.tight_layout()
    return ax
