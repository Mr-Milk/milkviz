from __future__ import annotations

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.cm import ScalarMappable
from matplotlib.collections import PatchCollection
from matplotlib.colors import Normalize, is_color_like

from legendkit import SizeLegend, Colorbar
from milkviz.utils import set_default


class DotHeatmap:

    def __init__(
            self,
            dot_size: np.ndarray,
            dot_hue: np.ndarray | str = None,
            matrix_hue: np.ndarray = None,
            xticklabels=None,
            yticklabels=None,
            xlabel=None,
            ylabel=None,
            sizes=(1, 200),
            size_norm=None,
            dtype=None,
            dot_patch="circle",
            dot_outline=True,
            outline_color=".8",
            alpha=1.0,
            dot_cmap=None,
            matrix_cmap=None,
            dot_norm=None,
            matrix_norm=None,
            dot_size_legend_kw=None,
            dot_hue_cbar_kw=None,
            matrix_cbar_kw=None,
            frameon=False,
            ax=None,
    ) -> None:
        self.ax = ax
        self.dot_size = dot_size
        self.dot_hue = dot_hue
        self.matrix_hue = matrix_hue
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.xticklabels = xticklabels
        self.yticklabels = yticklabels
        self.sizes = sizes
        self.dtype = dtype
        self.frameon = frameon

        self.dot_cmap = set_default(dot_cmap, "RdBu")
        self.matrix_cmap = set_default(matrix_cmap, "YlGn")
        self.dot_norm = dot_norm
        self.matrix_norm = matrix_norm

        self.dot_size_legend = None
        self.dot_hue_cbar = None
        self.matrix_cbar = None

        self.dot_size_legend_kw = set_default(dot_size_legend_kw, {})
        self.dot_hue_cbar_kw = set_default(dot_hue_cbar_kw, {})
        self.matrix_cbar_kw = set_default(matrix_cbar_kw, {})

        # init the grid
        self._set_grid()

        if matrix_hue is not None:
            rects = self.ax.pcolormesh(matrix_hue,
                                       cmap=matrix_cmap,
                                       norm=matrix_norm)

            self.add_matrix_cbar(rects)

        if dot_hue is not None:
            if is_color_like(dot_hue):
                circ_colors = np.repeat(dot_hue, dot_size.size)
            else:
                if not np.array((dot_hue.shape == dot_size.shape)).all():
                    raise ValueError(
                        "dot_hue does not match the shape of dot_size")
                c_array = dot_hue.flatten()
                if is_color_like(c_array[0]):
                    circ_colors = c_array
                else:
                    mapper = ScalarMappable(
                        norm=self.dot_norm,
                        cmap=self.dot_cmap
                    )
                    circ_colors = mapper.to_rgba(c_array)
                    self.add_dot_hue_cbar(mapper)

        else:
            circ_colors = np.repeat("C0", dot_size.size)

        if size_norm is None:
            size_norm = Normalize()
            size_norm.autoscale(dot_size)

        if dot_patch == "circle":
            circ_size = size_norm(dot_size) * (sizes[1] - sizes[0]) + sizes[0]
            self.ax.scatter(self.xcoord, self.ycoord,
                            s=circ_size, c=circ_colors)
            self.add_dot_size_legend()
        else:
            pie_sizes = size_norm(dot_size).flatten()
            pies = []
            for rx, ry, ratio, c in zip(self.xcoord,
                                        self.ycoord,
                                        pie_sizes,
                                        circ_colors):
                if (not np.isnan(ratio)) & (not np.ma.is_masked(ratio)):
                    pie = mpatches.Wedge((rx, ry), 0.4, -90, 360 * ratio,
                                         edgecolor=outline_color, facecolor=c,
                                         lw=0.5, alpha=alpha)
                    if dot_outline:
                        pie_bg = mpatches.Circle((rx, ry), 0.4,
                                                 edgecolor=outline_color,
                                                 facecolor="none", lw=0.5,
                                                 alpha=alpha)
                        pies.append(pie_bg)
                    pies.append(pie)
            self.ax.add_collection(PatchCollection(pies, match_original=True))

    def _set_grid(self):
        Y, X = self.dot_size.shape
        xticks = np.arange(X) + 0.5
        yticks = np.arange(Y) + 0.5
        x, y = np.meshgrid(xticks, yticks)  # Get the coordinates
        self.xcoord = x.flatten()
        self.ycoord = y.flatten()

        if self.ax is None:
            figsize = (0.5 * X, 0.5 * Y)
            _, self.ax = plt.subplots(figsize=figsize)
        if not self.frameon:
            for spine in self.ax.spines.values():
                spine.set_visible(0)

        self.ax.set_aspect("equal")
        self.ax.set_xlim(0, xticks[-1] + 0.5)
        self.ax.set_ylim(0, yticks[-1] + 0.5)
        self.ax.invert_yaxis()
        self.ax.set(xlabel=self.xlabel, ylabel=self.ylabel)

        if self.xticklabels is not None:
            self.ax.set_xticks(ticks=xticks, labels=self.xticklabels,
                               rotation=90, ha="center")
        else:
            self.ax.tick_params(axis="x", bottom=False, labelbottom=False)
        if self.yticklabels is not None:
            self.ax.set_yticks(ticks=yticks, labels=self.yticklabels)
        else:
            self.ax.tick_params(axis="y", left=False, labelleft=False)

    def add_dot_size_legend(self):
        options = dict(
            loc="out right upper",
        )
        options = {**options, **self.dot_size_legend_kw}
        self.dot_size_legend = SizeLegend(
            sizes=self.sizes,
            ax=self.ax,
            array=self.dot_size.flatten(),
            dtype=self.dtype,
            **options
        )

    def add_dot_hue_cbar(self, mapper):
        options = dict(
            orientation="vertical",
            loc="out right lower",
            width=0.3,
            height=1,
        )
        options = {**options, **self.dot_hue_cbar_kw}
        self.dot_hue_cbar = Colorbar(
            mapper,
            shape="ellipse",
            ax=self.ax,
            **options
        )

    def add_matrix_cbar(self, mapper):
        options = dict(
            orientation="horizontal",
            ticklocation="top",
            loc="out upper left",
        )
        options = {**options, **self.matrix_cbar_kw}
        self.matrix_cbar = Colorbar(mapper,
                                    ax=self.ax,
                                    **options
                                    )


def dot_heatmap(
        dot_size: np.ndarray,
        dot_hue: np.ndarray | str = None,
        matrix_hue: np.ndarray = None,
        xticklabels=None,
        yticklabels=None,
        xlabel=None,
        ylabel=None,
        sizes=(1, 200),
        size_norm=None,
        dtype=None,
        dot_patch="circle",
        dot_outline=True,
        outline_color=".8",
        alpha=1.0,
        dot_cmap=None,
        matrix_cmap=None,
        dot_norm=None,
        matrix_norm=None,
        dot_size_legend_kw=None,
        dot_hue_cbar_kw=None,
        matrix_cbar_kw=None,
        frameon=False,
        ax=None,
) -> DotHeatmap:
    """Dot heatmap + Matrix heatmap

    Parameters
    ----------
    dot_size : array-like
        2D array that define the size of dot or range of pie
    dot_hue : color, array-like color or number, default: "C0"
        Supply one color to make all dot in the same color,
        To config each one, supply a 2D array.
    matrix_hue : array-like
        The array that map to matrix colors
    xticklabels : array-like of str
    yticklabels : array-like of str
    xlabel : str
    ylabel : str
    sizes : tuple, default: (1, 200)
        The range of size to plot
    size_norm :
        A Normalize instance to scale sizes
    dtype :
    dot_patch : {"circle", "pie"}
        The style of dot
    dot_outline : bool, default: True
        Whether to draw the dot outline
    outline_color: , default: ".8"
        The color of the dot outline
    alpha : float
        Control the opacity
    dot_cmap : colormap, default: "RdBu"
        The colormap for dot
    matrix_cmap : colormap, default: "YlGn"
        The colormap for matrix
    dot_norm :
    matrix_norm :
    dot_size_legend_kw : dict
    dot_hue_cbar_kw : dict
    matrix_cbar_kw : dict
    frameon : bool, default: False
        Whether to draw the frame
    ax :

    Returns
    -------
    :class:`DotHeatmap`

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
        size_norm=size_norm,
        dtype=dtype,
        dot_patch=dot_patch,
        dot_outline=dot_outline,
        outline_color=outline_color,
        alpha=alpha,
        dot_cmap=dot_cmap,
        matrix_cmap=matrix_cmap,
        dot_norm=dot_norm,
        matrix_norm=matrix_norm,
        dot_size_legend_kw=dot_size_legend_kw,
        dot_hue_cbar_kw=dot_hue_cbar_kw,
        matrix_cbar_kw=matrix_cbar_kw,
        frameon=frameon,
        ax=ax,
    )
