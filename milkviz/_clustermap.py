from typing import List, Union, Optional, Tuple

import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import cm

from milkviz.utils import color_mapper_cat, set_cbar, set_category_legend


def anno_colors(info: pd.DataFrame, color: Union[str, List[str]]):
    uni_types = np.unique(info.to_numpy().flatten())
    colors_mapper = color_mapper_cat(color, uni_types)
    return info.replace(colors_mapper)


def anno_clustermap(
        df: pd.DataFrame,
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
        row_colors_legend_title: str = "rows",
        row_colors_legend_pos: Optional[Tuple[float, float, float, float]] = None,
        col_colors_legend_title: str = "cols",
        col_colors_legend_pos: Optional[Tuple[float, float, float, float]] = None,
        **kwargs,
) -> sns.matrix.ClusterGrid:
    # split the dataframe
    data = df.to_numpy()
    row_info = df.index.to_frame(index=False)
    col_info = df.columns.to_frame(index=False)
    row_label = row_info[row_label] if row_label is not None else None
    col_label = col_info[col_label] if col_label is not None else None
    plot_data = pd.DataFrame(data, index=row_label, columns=col_label)

    clustermap_kwargs = dict(cmap=heat_cmap, cbar_pos=None, **kwargs)
    row_colors_mapper = None
    col_colors_mapper = None

    if row_colors is not None:
        info = row_info[row_colors]
        uni_types = np.unique(info.to_numpy().flatten())
        row_colors_mapper = color_mapper_cat(row_colors_cmap, uni_types)
        clustermap_kwargs["row_colors"] = info.replace(row_colors_mapper)

    if col_colors is not None:
        info = col_info[col_colors]
        uni_types = np.unique(info.to_numpy().flatten())
        col_colors_mapper = color_mapper_cat(col_colors_cmap, uni_types)
        clustermap_kwargs["col_colors"] = info.replace(col_colors_mapper)

    g = sns.clustermap(plot_data, **clustermap_kwargs)
    cmin = np.nanmin(data)
    cmax = np.nanmax(data)
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
        set_category_legend(g.ax_heatmap, row_colors_mapper, bbox=row_colors_legend_pos,
                            title=row_colors_legend_title, marker="s")
    # plot col colors legend
    if col_colors is not None:
        col_colors_legend_pos = (1.02, 0.8, 0.1, 0.3) if col_colors_legend_pos is None else col_colors_legend_pos
        set_category_legend(g.ax_heatmap, col_colors_mapper, bbox=col_colors_legend_pos,
                            title=col_colors_legend_title, marker="s")

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
