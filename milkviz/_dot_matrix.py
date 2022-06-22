from typing import Literal, Optional, List, Union, Tuple, Any

import matplotlib as mpl
import matplotlib.axes
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import PathCollection, PatchCollection
from matplotlib.colors import Colormap, Normalize
from matplotlib.cm import ScalarMappable
from legendkit import SizeLegend, Colorbar, EllipseColorbar

from milkviz._dot import set_dot_grid
from milkviz.types import Pos, Size
from milkviz.utils import doc, norm_arr, set_cbar, set_size_legend, set_circle_cbar, set_default, set_spines, set_ticks


class DotHeatmap:
    matrix: np.ndarray
    dot_size: np.ndarray
    dot_hue: np.ndarray
    
    def __init__(
        self,
        dot_size: np.ndarray,
        dot_hue: np.ndarray = None,
        matrix_hue: Optional[np.ndarray] = None,
        xticklabels: Optional[List[str]] = None,
        yticklabels: Optional[List[str]] = None,
        xlabel: Optional[str] = None,
        ylabel: Optional[str] = None,
        sizes: Tuple[int, int] = (1, 100),
        dtype: Any = None,
        dot_patch: Literal["circle", "pie"] = "circle",
        edgecolor: Any = "#999999",
        alpha: float = 1.0,
        dot_cmap: Union[str, Colormap, None] = None,
        matrix_cmap: Union[str, Colormap, None] = None,
        # legend_title: Optional[str] = None,
        # legend_pos: Pos = None,
        # hue_cbar_title: Optional[str] = None,
        # hue_cbar_ticklabels: Optional[List[str]] = None,
        # hue_cbar_pos: Pos = None,
        # hue_cbar_size: Size = None,
        # matrix_cbar_title: Optional[str] = None,
        # matrix_cbar_ticklabels: Optional[List[str]] = None,
        # matrix_cbar_pos: Optional[Tuple] = None,
        # matrix_cbar_size: Size = None,
        no_spines: bool = True,
        no_ticks: bool = True,
        ax: Optional[mpl.axes.Axes] = None,
    ) -> None:
        if ax is None:
            ax = plt.gca()
        self.ax = ax
        self.dot_size = dot_size
        self.dot_hue = dot_hue
        self.matrix_hue = matrix_hue
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.xticklabels = xticklabels if xticklabels is not None else []
        self.yticklabels = yticklabels if yticklabels is not None else []
        self.sizes = sizes
        self.no_spines = no_spines
        self.no_ticks = no_ticks

        self.dot_cmap = set_default(dot_cmap, "RdBu")
        self.matrix_cmap = set_default(matrix_cmap, "YlGn")

        # init the grid
        self._set_grid()

        show_dot_hue_cbar = False

        if dot_hue is not None:
            if isinstance(dot_hue, str):
                circ_colors = np.repeat(dot_hue, dot_size.size)
            else:
                if np.array((dot_hue.shape == dot_size.shape)).all():
                    show_dot_hue_cbar = True
                    c_array = dot_hue.flatten()
                    cmin = np.nanmin(c_array)
                    cmax = np.nanmax(c_array)
                    mapper = ScalarMappable(Normalize(vmin=cmin, vmax=cmax), cmap=self.dot_cmap)
                    circ_colors = mapper.to_rgba(c_array)

                    self.add_dot_hue_cbar(cmin, cmax)
                else:
                    raise ValueError("dot_hue does not match the shape of dot_size")
        else:
            circ_colors = np.repeat("#D75455", dot_size.size)

        if dot_patch == "circle":
            circ_size = norm_arr(dot_size, sizes)
            self.ax.scatter(self.xcoord, self.ycoord, s=circ_size, c=circ_colors)
            self.add_dot_size_legend()
        else:
            norm_sizes = norm_arr(dot_size, size=(0, 1))
            for rx, ry, ratio, c in zip(self.xcoord, self.ycoord, norm_sizes, circ_colors):
                pie = mpatches.Wedge((rx, ry), 0.4, 90, 360*ratio+90, edgecolor=edgecolor, facecolor=c, lw=0.5, alpha=alpha)
                self.ax.add_artist(pie)
            

        if matrix_hue is not None:
            rects = [mpatches.Rectangle((rx - 0.5, ry - 0.5), 1, 1) \
                for rx, ry in zip(self.xcoord, self.ycoord)]
            rects_colors = matrix_hue.flatten()
            rects_cmin = np.nanmin(rects_colors)
            rects_cmax = np.nanmax(rects_colors)
            rects = PatchCollection(rects, array=rects_colors, cmap=self.matrix_cmap, alpha=alpha)
            rects.set_clim(rects_cmin, rects_cmax)
            rects.set_zorder(-1)
            self.ax.add_collection(rects)

            self.add_matrix_cbar(rects)
            

    def _set_grid(self):
        Y, X = self.dot_size.shape
        x, y = np.meshgrid(np.arange(X), np.arange(Y))  # Get the coordinates
        self.xcoord = x.flatten()
        self.ycoord = y.flatten()

        if self.ax is None:
            figsize = (0.4 * X + 2, 0.4 * Y + 1)
            _, self.ax = plt.subplots(figsize=figsize)
        if self.no_spines:
            set_spines(self.ax)
        if self.no_ticks:
            set_ticks(self.ax)
        self.ax.set_aspect("equal")
        self.ax.set_xlim(-0.5, X - 0.5)
        self.ax.set_ylim(-0.5, Y - 0.5)
        self.ax.set(xlabel=self.xlabel, ylabel=self.ylabel)
        self.ax.set_xticks(np.arange(X), labels=self.xticklabels, rotation=90, ha="center")
        self.ax.set_yticks(np.arange(Y), labels=self.yticklabels)

    
    def add_dot_size_legend(self):
        self.dot_size_legend = SizeLegend(self.sizes, 
        ax=self.ax,
        bbox_to_anchor=(1.05, 1),
        loc="upper left",
        bbox_transform=self.ax.transAxes)

    def add_dot_hue_cbar(self, vmin, vmax):
        self.dot_hue_cbar = EllipseColorbar(vmin=vmin, vmax=vmax, cmap=self.dot_cmap, ax=self.ax)

    def add_dot_hue_legend(self):
        pass

    def add_matrix_cbar(self, cmapping):
        self.matrix_cbar = Colorbar(cmapping,
        ax=self.ax,
        orientation="vertical",
        loc="lower left",
        bbox_to_anchor=(1.05, 0),
        bbox_transform=self.ax.transAxes,
        )


@doc
def dot_heatmap(
        dot_size: np.ndarray,
        dot_hue: np.ndarray,
        matrix_hue: Optional[np.ndarray] = None,
        xticklabels: Optional[List[str]] = None,
        yticklabels: Optional[List[str]] = None,
        xlabel: Optional[str] = None,
        ylabel: Optional[str] = None,
        sizes: Tuple[int, int] = (1, 100),
        dtype: Any = None,
        dot_cmap: Union[str, Colormap, None] = None,
        dot_patch: str = "circle",
        matrix_cmap: Union[str, Colormap, None] = None,
        alpha=1,
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
    # dot_cmap = set_default(dot_cmap, "RdBu")
    # matrix_cmap = set_default(matrix_cmap, "YlGn")
    # ax, xcoord, ycoord = set_dot_grid(dot_size, ax=ax, xlabel=xlabel, ylabel=ylabel,
    #                                   xticklabels=xticklabels, yticklabels=yticklabels,
    #                                   no_spines=no_spines, no_ticks=no_ticks)

    # circ_size = norm_arr(dot_size, sizes)
    # circ_colors = dot_hue.flatten()
    # circles = plt.scatter(xcoord, ycoord, s=circ_size, c=circ_colors, cmap=dot_cmap)
    # # adding dot size legend
    # set_size_legend(ax, dot_size, circ_size, pos=legend_pos, title=legend_title, dtype=dtype)

    # # adding dot colorbar
    # if (hue_cbar_pos is None) & (matrix_hue is None):
    #     hue_cbar_pos = (1.05, 0)
    # elif hue_cbar_pos is None:
    #     hue_cbar_pos = (1.05, 0.4)
    # matrix_cbar_pos = (1.05, 0) if matrix_cbar_pos is None else matrix_cbar_pos
    # if matrix_hue is None:
    #     set_cbar(ax,
    #              patches=circles,
    #              c_array=circ_colors,
    #              bbox=hue_cbar_pos,
    #              size=hue_cbar_size,
    #              title=hue_cbar_title,
    #              ticklabels=hue_cbar_ticklabels,
    #              cmap=dot_cmap)
    # else:
    #     set_circle_cbar(ax,
    #                     c_array=circ_colors,
    #                     bbox=hue_cbar_pos, size=hue_cbar_size,
    #                     title=hue_cbar_title,
    #                     ticklabels=hue_cbar_ticklabels,
    #                     cmap=dot_cmap)

    # if matrix_hue is not None:
    #     rects = [mpatches.Rectangle((rx - 0.5, ry - 0.5), 1, 1) for rx, ry in zip(xcoord, ycoord)]
    #     rects_colors = matrix_hue.flatten()
    #     rects_cmin = np.nanmin(rects_colors)
    #     rects_cmax = np.nanmax(rects_colors)
    #     rects = PatchCollection(rects, array=rects_colors, cmap=matrix_cmap)
    #     rects.set_clim(rects_cmin, rects_cmax)
    #     rects.set_zorder(-1)
    #     ax.add_collection(rects)

    #     set_cbar(ax,
    #              patches=rects,
    #              c_array=rects_colors,
    #              bbox=matrix_cbar_pos,
    #              size=matrix_cbar_size,
    #              title=matrix_cbar_title,
    #              ticklabels=matrix_cbar_ticklabels,
    #              cmap=matrix_cmap
    #              )
    # plt.tight_layout()
    # return ax
    h = DotHeatmap(
        dot_size,
        dot_hue,
        matrix_hue=matrix_hue,
        xticklabels=xticklabels,
        yticklabels=yticklabels,
        xlabel=xlabel,
        ylabel=ylabel,
        sizes=sizes,
        dtype=dtype,
        dot_patch=dot_patch,
        edgecolor = "#999999",
        alpha=alpha,
        dot_cmap = dot_cmap,
        matrix_cmap = matrix_cmap,
        )

    return h
