from typing import List, Union, Optional, Tuple

import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import cm

from milkviz.utils import color_mapper_cat, set_cbar, set_category_legend, doc


def anno_colors(info: pd.DataFrame, color: Union[str, List[str]]):
    uni_types = np.unique(info.to_numpy().flatten())
    colors_mapper = color_mapper_cat(color, uni_types)
    return info.replace(colors_mapper)


def move_bbox(bbox, move_index, amount):
    bbox = list(bbox)
    bbox[move_index] += amount
    return tuple(bbox)


@doc
def anno_clustermap(
        data: pd.DataFrame,
        row_colors: Union[str, List[str], None] = None,
        row_label: Optional[str] = None,
        col_colors: Union[str, List[str], None] = None,
        col_label: Optional[str] = None,
        heat_cmap: str = "RdBu_r",
        row_colors_cmap: Union[str, List[str]] = "tab20",
        col_colors_cmap: Union[str, List[str]] = "Set2",
        categorical_cbar: Optional[List[str]] = None,
        cbar_title: str = "data",
        cbar_pos: Optional[Tuple[float, float, float, float]] = None,
        row_colors_legend_pos: Optional[Tuple[float, float, float, float]] = None,
        col_colors_legend_pos: Optional[Tuple[float, float, float, float]] = None,
        legend_padding = 0.2,
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
        cbar_pos: The colorbar position
        row_colors_legend_pos: row_colors' legend's position, default is (1.02, 0.35, 0.1, 0.3)
        col_colors_legend_pos: col_colors' legend's position, default is (1.02, 0.7, 0.1, 0.3)
        legend_padding: Use to specific the padding between multiple row/col legends
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
    row_colors_legend_contents = None
    col_colors_legend_contents = None

    if row_colors is not None:
        info = row_info[row_colors]
        row_colors_legend_contents = {rc: np.unique(info[rc].to_numpy().flatten()) for rc in row_colors}
        uni_types = np.unique(info.to_numpy().flatten())
        row_colors_mapper = color_mapper_cat(row_colors_cmap, uni_types)
        clustermap_kwargs["row_colors"] = info.replace(row_colors_mapper)

    if col_colors is not None:
        info = col_info[col_colors]
        col_colors_legend_contents = {cc: np.unique(info[cc].to_numpy().flatten()) for cc in col_colors}
        uni_types = np.unique(info.to_numpy().flatten())
        col_colors_mapper = color_mapper_cat(col_colors_cmap, uni_types)
        clustermap_kwargs["col_colors"] = info.replace(col_colors_mapper)

    g = sns.clustermap(plot_data, **clustermap_kwargs)
    cmin = np.nanmin(plot_data)
    cmax = np.nanmax(plot_data)
    cbar_pos = (1.05, 0.0, 0.05, 0.15) if cbar_pos is None else cbar_pos
    if categorical_cbar is not None:
        cmap = cm.get_cmap(heat_cmap)
        cmap_size = np.linspace(0, cmap.N, len(categorical_cbar), dtype=int)
        cmapper = dict(zip(categorical_cbar, [cmap(i) for i in cmap_size]))
        set_category_legend(g.ax_heatmap, cmapper, bbox=cbar_pos, title=cbar_title, marker="s")
    else:
        set_cbar(g.ax_heatmap, bbox=cbar_pos, cmin=cmin, cmax=cmax, cmap=heat_cmap)

    # plot row colors legend
    if row_colors is not None:
        row_colors_legend_pos = (1.02, 0.35, 0.1, 0.3) if row_colors_legend_pos is None else row_colors_legend_pos
        row_colors_legend_pos = move_bbox(row_colors_legend_pos, 0, -legend_padding)
        for k, v in row_colors_legend_contents.items():
            row_colors_legend_pos = move_bbox(row_colors_legend_pos, 0, legend_padding)
            row_cmapper = {i: row_colors_mapper[i] for i in v}
            set_category_legend(g.ax_heatmap, row_cmapper, bbox=row_colors_legend_pos,
                                title=k, marker="s")
    # plot col colors legend
    if col_colors is not None:
        col_colors_legend_pos = (1.02, 0.7, 0.1, 0.3) if col_colors_legend_pos is None else col_colors_legend_pos
        col_colors_legend_pos = move_bbox(col_colors_legend_pos, 0, -legend_padding)
        for k, v in col_colors_legend_contents.items():
            col_colors_legend_pos = move_bbox(col_colors_legend_pos, 0, legend_padding)
            col_cmapper = {i: col_colors_mapper[i] for i in v}
            set_category_legend(g.ax_heatmap, col_cmapper, bbox=col_colors_legend_pos,
                                title=k, marker="s")

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
