from __future__ import annotations

from typing import Literal, Optional, List, Union, Tuple, Any, Dict

import matplotlib as mpl
import matplotlib.axes
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.cm import ScalarMappable
from matplotlib.collections import PatchCollection
from matplotlib.colors import Colormap, Normalize, is_color_like

from legendkit import SizeLegend, Colorbar, EllipseColorbar
from milkviz.utils import doc, norm_arr, set_default, set_spines, set_ticks

DotPatch = Literal["circle", "pie"]


class DotHeatmap:

    def __init__(
            self,
            dot_size: np.ndarray,
            dot_hue: np.ndarray = None,
            matrix_hue: np.ndarray = None,
            xticklabels: List[str] = None,
            yticklabels: List[str] = None,
            xlabel: str = None,
            ylabel: str = None,
            sizes: Tuple[int, int] = (1, 200),
            dtype: Any = None,
            dot_patch: DotPatch = "circle",
            dot_outline: bool = True,
            outline_color: Any = "#999999",
            alpha: float = 1.0,
            dot_cmap: Union[str, Colormap, None] = None,
            matrix_cmap: Union[str, Colormap, None] = None,
            dot_size_legend_kw: Dict = None,
            dot_hue_cbar_kw: Dict = None,
            matrix_cbar_kw: Dict = None,
            no_spines: bool = True,
            no_ticks: bool = True,
            ax: Optional[mpl.axes.Axes] = None,
    ) -> None:
        self.ax = ax
        self.dot_size = dot_size
        self.dot_hue = dot_hue
        self.matrix_hue = matrix_hue
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.xticklabels = xticklabels if xticklabels is not None else []
        self.yticklabels = yticklabels if yticklabels is not None else []
        self.sizes = sizes
        self.dtype = dtype
        self.no_spines = no_spines
        self.no_ticks = no_ticks

        self.dot_cmap = set_default(dot_cmap, "RdBu")
        self.matrix_cmap = set_default(matrix_cmap, "YlGn")

        self.dot_size_legend = None
        self.dot_hue_cbar = None
        self.matrix_cbar = None

        self.dot_size_legend_kw = set_default(dot_size_legend_kw, {})
        self.dot_hue_cbar_kw = set_default(dot_hue_cbar_kw, {})
        self.matrix_cbar_kw = set_default(matrix_cbar_kw, {})

        # init the grid
        self._set_grid()

        if dot_hue is not None:
            if isinstance(dot_hue, str):
                circ_colors = np.repeat(dot_hue, dot_size.size)
            else:
                if np.array((dot_hue.shape == dot_size.shape)).all():
                    c_array = dot_hue.flatten()
                    if is_color_like(c_array[0]):
                        circ_colors = c_array
                    else:
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
                if not np.isnan(ratio):
                    pie = mpatches.Wedge((rx, ry), 0.4, 90, 360 * ratio + 90, edgecolor=outline_color, facecolor=c, lw=0.5,
                                         alpha=alpha)
                    if dot_outline:
                        pie_bg = mpatches.Circle((rx, ry), 0.4, edgecolor=outline_color, facecolor="none", lw=0.5,
                                                 alpha=alpha)
                        self.ax.add_artist(pie_bg)
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
            figsize = (0.5 * X, 0.5 * Y)
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
        options = dict(
            bbox_to_anchor=(1.05, 1),
            loc="upper left",
            bbox_transform=self.ax.transAxes,
            title_align="left"
        )
        options = {**options, **self.dot_size_legend_kw}
        self.dot_size_legend = SizeLegend(self.sizes,
                                          ax=self.ax,
                                          array=self.dot_size,
                                          dtype=self.dtype,
                                          **options
                                          )

    def add_dot_hue_cbar(self, vmin, vmax):
        options = dict(
            orientation="vertical",
            bbox_to_anchor=(1.05, 0),
            loc="lower left",
            bbox_transform=self.ax.transAxes,
            title_align="left"
        )
        options = {**options, **self.dot_hue_cbar_kw}
        self.dot_hue_cbar = EllipseColorbar(vmin=vmin,
                                            vmax=vmax,
                                            cmap=self.dot_cmap,
                                            ax=self.ax,
                                            **options
                                            )

    def add_matrix_cbar(self, cmapping):
        options = dict(
            orientation="horizontal",
            ticklocation="top",
            loc="lower left",
            bbox_to_anchor=(0, 1.05),
            bbox_transform=self.ax.transAxes,
            title_align="left"
        )
        options = {**options, **self.matrix_cbar_kw}
        self.matrix_cbar = Colorbar(cmapping,
                                    ax=self.ax,
                                    **options
                                    )


@doc
def dot_heatmap(
        dot_size: np.ndarray,
        dot_hue: np.ndarray = None,
        matrix_hue: np.ndarray = None,
        xticklabels: List[str] = None,
        yticklabels: List[str] = None,
        xlabel: str = None,
        ylabel: str = None,
        sizes: Tuple[int, int] = (1, 200),
        dtype: Any = None,
        dot_patch: DotPatch = "circle",
        dot_outline: bool = True,
        outline_color: Any = "#999999",
        alpha: float = 1.0,
        dot_cmap: Union[str, Colormap, None] = None,
        matrix_cmap: Union[str, Colormap, None] = None,
        dot_size_legend_kw: Dict = None,
        dot_hue_cbar_kw: Dict = None,
        matrix_cbar_kw: Dict = None,
        no_spines: bool = True,
        no_ticks: bool = True,
        ax: mpl.axes.Axes = None,
) -> DotHeatmap:
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
        dot_patch: The dot will be drawn as "circle" or "pie"
        dot_outline: To draw the dot outline, Default: True
        outline_color: The color of the dot outline, Default: "#999999"
        alpha: Control the opacity
        dot_cmap: The colormap for dot, default: "RdBu"
        matrix_cmap: The colormap for matrix, default: "YlGn"
        dot_size_legend_kw:
        dot_hue_cbar_kw:
        matrix_cbar_kw:
        no_spines: [no_spines]
        no_ticks: [no_ticks]
        ax: [ax]

    Returns:
        Return a `DotHeatmap` object

    """

    return DotHeatmap(
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
        dot_outline=dot_outline,
        outline_color=outline_color,
        alpha=alpha,
        dot_cmap=dot_cmap,
        matrix_cmap=matrix_cmap,
        dot_size_legend_kw=dot_size_legend_kw,
        dot_hue_cbar_kw=dot_hue_cbar_kw,
        matrix_cbar_kw=matrix_cbar_kw,
        no_spines=no_spines,
        no_ticks=no_ticks,
        ax=ax
    )


@doc
def dot(
        dot_size: np.ndarray,
        dot_hue: np.ndarray = None,
        xticklabels: List[str] = None,
        yticklabels: List[str] = None,
        xlabel: str = None,
        ylabel: str = None,
        sizes: Tuple[int, int] = (1, 200),
        dtype: Any = None,
        dot_patch: DotPatch = "circle",
        dot_outline: bool = True,
        outline_color: Any = "#999999",
        alpha: float = 1.0,
        legend_kw: Dict = None,
        no_spines: bool = True,
        no_ticks: bool = True,
        ax: mpl.axes.Axes = None,
) -> DotHeatmap:
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
        dot_patch: The dot will be drawn as "circle" or "pie"
        dot_outline: To draw the dot outline, Default: True
        outline_color: The color of the dot outline, Default: "#999999"
        alpha: Control the opacity
        legend_kw: The options that pass to control legend, should be a dict
        no_spines: [no_spines]
        no_ticks: [no_ticks]
        ax: [ax]

    Returns:
        Return a `DotHeatmap` object

    """

    return DotHeatmap(
        dot_size,
        dot_hue,
        xticklabels=xticklabels,
        yticklabels=yticklabels,
        xlabel=xlabel,
        ylabel=ylabel,
        sizes=sizes,
        dtype=dtype,
        dot_patch=dot_patch,
        outline_color=outline_color,
        alpha=alpha,
        dot_outline=dot_outline,
        dot_size_legend_kw=legend_kw,
        no_spines=no_spines,
        no_ticks=no_ticks,
        ax=ax
    )
