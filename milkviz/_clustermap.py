from typing import List, Union, Optional, Tuple

import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import cm
from matplotlib.colors import Colormap

from milkviz.utils import color_mapper_cat, set_cbar, set_category_legend, doc


def anno_colors(info: pd.DataFrame, color: Union[str, List[str]]):
    uni_types = np.unique(info.to_numpy().flatten())
    colors_mapper = color_mapper_cat(color, uni_types)
    return info.replace(colors_mapper)


def move_bbox(bbox, move_index, amount):
    bbox = list(bbox)
    bbox[move_index] += amount
    return tuple(bbox)


def color_legend_split(ax, legend_pos, legend_contents, colors_mapper, padding):
    extend_ncol = {1: 1, 2: 1.5, 3: 2}
    ncol = 1
    legend_pos = move_bbox(legend_pos, 0, -padding)
    for k, v in legend_contents.items():
        legend_pos = move_bbox(legend_pos, 0, padding)
        cmapper = {i: colors_mapper[i] for i in v}
        padding /= ncol  # reset the padding
        ncol = set_category_legend(ax, cmapper, bbox=legend_pos,
                                   title=k, marker="s")
        padding *= extend_ncol[ncol]  # if ncol > 1, extend the padding


def color_legend(ax, legend_pos, legend_contents, colors_mapper, title=None):
    cmapper = {}
    for k, v in legend_contents.items():
        for i in v:
            cmapper[i] = colors_mapper[i]
    set_category_legend(ax, cmapper, bbox=legend_pos, title=title, marker="s")


@doc
def anno_clustermap(
        data: pd.DataFrame,
        row_colors: Union[str, List[str], None] = None,
        row_label: Optional[str] = None,
        col_colors: Union[str, List[str], None] = None,
        col_label: Optional[str] = None,
        heat_cmap: Union[str, Colormap] = "RdBu_r",
        row_colors_cmap: Union[str, List[str]] = "tab20",
        col_colors_cmap: Union[str, List[str]] = "tab20",
        categorical_cbar: Optional[List[str]] = None,
        cbar_title: str = "data",
        cbar_pos: Optional[Tuple[float, float, float, float]] = None,
        row_legend_pos: Optional[Tuple[float, float, float, float]] = None,
        col_legend_pos: Optional[Tuple[float, float, float, float]] = None,
        row_legend_title: str = "row",
        col_legend_title: str = "col",
        row_legend_split: bool = True,
        col_legend_split: bool = True,
        row_legend_padding: float = 0.25,
        col_legend_padding: float = 0.25,
        **kwargs,
) -> sns.matrix.ClusterGrid:
    """Color or label annotated clustermap

    Args:
        data: [data], multi-levels annotations should store in MultiIndex
        row_colors: The index level used to label rows in color stripe
        row_label: The index level used for x-axis label
        col_colors: The columns level used to label columns in color stripe
        col_label: The columns level used for y-axis label
        heat_cmap: The colormap for heatmap
        row_colors_cmap: The colormap for row_colors
        col_colors_cmap: The colormap for col_colors
        categorical_cbar: Turn the colorbar in to categorical legend in text
        cbar_title: The colorbar title
        cbar_pos: The colorbar position, default is (1.05, 0.0, 0.05, 0.15)
        row_legend_title: The title of row legend, when row_legend_split = False
        col_legend_title: The title of col legend, when col_legend_split = False
        row_legend_pos: row_colors' legend's position, default is (0.02, -0.36, 0.1, 0.3)
        col_legend_pos: col_colors' legend's position, default is (1.05, 0.7, 0.1, 0.3)
        row_legend_split: Whether to split each level of row legend
        col_legend_split: Whether to split each level of col legend
        row_legend_padding: Use to specific the padding between multiple row/col legends
        col_legend_padding: Use to specific the padding between multiple row/col legends
        **kwargs: Pass to `seaborn.clustermap <https://seaborn.pydata.org/generated/seaborn.clustermap.html#seaborn.clustermap>`_

    Returns:
        A `seaborn.matrix.ClusterGrid` instance

    """
    # split the dataframe
    raw_data = data.to_numpy()
    row_info = data.index.to_frame(index=False)
    col_info = data.columns.to_frame(index=False)
    row_label = row_info[row_label] if row_label is not None else None
    col_label = col_info[col_label] if col_label is not None else None
    plot_data = pd.DataFrame(raw_data, index=row_label, columns=col_label)

    clustermap_kwargs = dict(cmap=heat_cmap, cbar_pos=None, **kwargs)
    row_colors_mapper = None
    col_colors_mapper = None
    row_legend_contents = None
    col_legend_contents = None

    if row_colors is not None:
        info = row_info[row_colors]
        row_legend_contents = {rc: np.unique(info[rc].to_numpy().flatten()) for rc in row_colors}
        row_colors_mapper = color_mapper_cat(info.to_numpy().flatten(), cmap=row_colors_cmap)
        clustermap_kwargs["row_colors"] = info.replace(row_colors_mapper)

    if col_colors is not None:
        info = col_info[col_colors]
        col_legend_contents = {cc: np.unique(info[cc].to_numpy().flatten()) for cc in col_colors}
        col_colors_mapper = color_mapper_cat(info.to_numpy().flatten(), cmap=col_colors_cmap)
        clustermap_kwargs["col_colors"] = info.replace(col_colors_mapper)

    g = sns.clustermap(plot_data, **clustermap_kwargs)
    cmin = np.nanmin(plot_data)
    cmax = np.nanmax(plot_data)
    cbar_pos = (1.05, 0.0, 0.05, 0.15) if cbar_pos is None else cbar_pos
    if categorical_cbar is not None:
        cmap = cm.get_cmap(heat_cmap)
        cmap_size = np.linspace(0, cmap.N, len(categorical_cbar), dtype=int)
        cmapper = dict(zip(categorical_cbar, [cmap(i) for i in cmap_size]))
        set_category_legend(g.ax_heatmap, cmapper, bbox=cbar_pos,
                            title=cbar_title, marker="s", reverse=True)
    else:
        set_cbar(g.ax_heatmap, bbox=cbar_pos, cmin=cmin, cmax=cmax, cmap=heat_cmap, title=cbar_title)

    # plot row colors legend
    if row_colors is not None:
        row_legend_pos = (0.02, -0.36, 0.1, 0.3) if row_legend_pos is None else row_legend_pos
        if row_legend_split:
            color_legend_split(g.ax_heatmap, row_legend_pos, row_legend_contents,
                               row_colors_mapper, row_legend_padding)
        else:
            color_legend(g.ax_heatmap, row_legend_pos, row_legend_contents,
                         row_colors_mapper, row_legend_title)
    # plot col colors legend
    if col_colors is not None:
        col_legend_pos = (1.05, 0.7, 0.1, 0.3) if col_legend_pos is None else col_legend_pos
        if col_legend_split:
            color_legend_split(g.ax_heatmap, col_legend_pos, col_legend_contents,
                               col_colors_mapper, col_legend_padding)
        else:
            color_legend(g.ax_heatmap, col_legend_pos, col_legend_contents,
                         col_colors_mapper, col_legend_title)

    # close labels and ticks on y-axis
    if row_label is None:
        g.ax_heatmap.set_yticklabels("")
        g.ax_heatmap.set_ylabel("")
        g.ax_heatmap.set_yticks([])

    # close labels and ticks on x-axis
    if col_label is None:
        g.ax_heatmap.set_xticklabels("")
        g.ax_heatmap.set_xlabel("")
        g.ax_heatmap.set_xticks([])

    return g
