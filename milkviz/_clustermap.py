from typing import List, Union, Optional, Dict

import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import cm

from milkviz.types import Pos, Colors, Text, Size
from milkviz.utils import color_mapper_cat, set_cbar, doc, set_category_square_legend


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
        ncol = set_category_square_legend(ax, cmapper, pos=legend_pos, title=k)
        padding *= extend_ncol[ncol]  # if ncol > 1, extend the padding


@doc
def anno_clustermap(
        data: pd.DataFrame,
        # define row colors
        row_colors: Union[str, List[str], None] = None,
        row_colors_cmap: Union[str, List[str], None] = None,
        row_colors_order: Optional[Dict] = None,
        row_colors_label: Optional[Dict] = None,
        row_label: Optional[str] = None,
        row_legend_pos: Pos = None,
        row_legend_title: Optional[str] = None,
        row_legend_split: bool = True,
        row_legend_padding: float = 0.25,
        # define col colors
        col_colors: Union[str, List[str], None] = None,
        col_colors_cmap: Union[str, List[str], None] = None,
        col_colors_order: Optional[Dict] = None,
        col_colors_label: Optional[Dict] = None,
        col_label: Optional[str] = None,
        col_legend_pos: Pos = None,
        col_legend_title: Optional[str] = None,
        col_legend_split: bool = True,
        col_legend_padding: float = 0.25,

        heat_cmap: Colors = None,
        categorical_cbar: Optional[List[str]] = None,
        cbar_title: Text = None,
        cbar_ticklabels: Optional[List[str]] = None,
        cbar_pos: Pos = None,
        cbar_size: Size = None,

        **kwargs,
) -> sns.matrix.ClusterGrid:
    """Color or label annotated clustermap

    Args:
        data: [data], multi-levels annotations should store in MultiIndex
        {row|col}_label: The index/columns level used for x-axis/y-axis label
        {row|col}_colors: The index/columns level used to label in color stripe
        row_colors_cmap: The colormap for row_colors, default: "tab20"
        col_colors_cmap: The colormap for col_colors, default: "echarts", a custom colormap in milkviz
        {row|col}_colors_order: A dict-like mapper to specific the order in each level,
        {row|col}_colors_label: A dict-like mapper to overwrite the name of each level,
        {row|col}_legend_split: Whether to split each level of colors stripe
        {row|col}_legend_title: The title of row legend, when row_legend_split = False
        {row|col}_legend_pos: row_colors' legend's position, default is row: (1.05, 0.3) col: (1.05, 0.7)
        {row|col}_legend_padding: Use to specific the padding between multiple row/col legends

        heat_cmap: The colormap for heatmap, default: "RdBu_r"
        categorical_cbar: Turn the colorbar in to categorical legend in text
        cbar_title: [cbar_title]
        cbar_ticklabels: Overwrite the ticklabels on colorbar
        cbar_pos: [cbar_pos]
        cbar_size: [cbar_size]
        **kwargs: Pass to `seaborn.clustermap <https://seaborn.pydata.org/generated/seaborn.clustermap.html#seaborn.clustermap>`_

    Returns:
        A `seaborn.matrix.ClusterGrid` instance

    """
    row_colors_cmap = "tab20" if row_colors_cmap is None else row_colors_cmap
    col_colors_cmap = "echarts" if col_colors_cmap is None else col_colors_cmap
    heat_cmap = "RdBu_r" if heat_cmap is None else heat_cmap

    # split the dataframe
    data = data.copy()
    raw_data = data.to_numpy()

    if isinstance(row_colors, str):
        row_colors = [row_colors]

    if isinstance(col_colors, str):
        col_colors = [col_colors]

    if (row_colors is not None) & (row_colors_order is not None):
        # data.reorder_levels(list(row_colors_order.keys()), axis=0)
        for name, labels in row_colors_order.items():
            data = data.reindex(axis="index", level=name, labels=labels)

    if (col_colors is not None) & (col_colors_order is not None):
        # data.reorder_levels(list(col_colors_order.keys()), axis=1)
        for name, labels in col_colors_order.items():
            data = data.reindex(axis="column", level=name, labels=labels)

    if (row_colors is not None) & (row_colors_label is not None):
        data = data.rename_axis(index=row_colors_label)
        row_colors = [row_colors_label[label] for label in row_colors]

    if (col_colors is not None) & (col_colors_label is not None):
        data = data.rename_axis(columns=col_colors_label)
        col_colors = [col_colors_label[label] for label in col_colors]

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

    if categorical_cbar is not None:
        cbar_pos = (1.05, -0.9) if cbar_pos is None else cbar_pos
        cmap = cm.get_cmap(heat_cmap)
        cmap_size = np.linspace(0, cmap.N, len(categorical_cbar), dtype=int)
        cmapper = dict(zip(categorical_cbar, [cmap(i) for i in cmap_size]))
        set_category_square_legend(g.ax_heatmap,
                                   cmapper,
                                   pos=cbar_pos,
                                   title=cbar_title,
                                   reverse=True)
    else:
        cbar_pos = (1.05, 0) if cbar_pos is None else cbar_pos
        set_cbar(g.ax_heatmap,
                 bbox=cbar_pos,
                 size=cbar_size,
                 c_array=g.data2d.to_numpy(),
                 cmap=heat_cmap,
                 title=cbar_title,
                 ticklabels=cbar_ticklabels,
                 )

    # plot row colors legend
    if row_colors is not None:
        row_legend_pos = (1.05, -0.4) if row_legend_pos is None else row_legend_pos
        if row_legend_split:
            color_legend_split(g.ax_heatmap, row_legend_pos, row_legend_contents,
                               row_colors_mapper, row_legend_padding)
        else:
            title = row_colors[0] if row_legend_title is None else row_legend_title
            set_category_square_legend(g.ax_heatmap,
                                       row_colors_mapper,
                                       pos=row_legend_pos,
                                       title=title, )
    # plot col colors legend
    if col_colors is not None:
        col_legend_pos = (1.05, 0) if col_legend_pos is None else col_legend_pos
        if col_legend_split:
            color_legend_split(g.ax_heatmap, col_legend_pos, col_legend_contents,
                               col_colors_mapper, col_legend_padding)
        else:
            title = col_colors[0] if col_legend_title is None else col_legend_title
            set_category_square_legend(g.ax_heatmap,
                                       col_colors_mapper,
                                       pos=col_legend_pos,
                                       title=title, )

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
