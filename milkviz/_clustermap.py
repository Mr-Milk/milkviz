from __future__ import annotations

from typing import List, Optional, Dict, Any

import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import cm

from legendkit import CatLegend, Colorbar, vstack, hstack
from milkviz.utils import color_mapper_cat, doc, set_default


@doc
def anno_clustermap(
        data: pd.DataFrame,
        # define row colors
        row_colors: str | List[str] = None,
        row_colors_cmap: str | List[str] = None,
        row_colors_order: Dict = None,
        row_colors_label: Dict = None,
        row_label: str = None,
        row_legend_title: str = None,
        row_legend_split: bool = True,
        # define col colors
        col_colors: str | List[str] = None,
        col_colors_cmap: str | List[str] = None,
        col_colors_order: Dict = None,
        col_colors_label: Dict = None,
        col_label: str = None,
        col_legend_title: str = None,
        col_legend_split: bool = True,
        heat_cmap: Any = None,
        legend_padding: float = 5,
        legend_kw: Dict = None,
        cbar_kw: Dict = None,
        categorical_cbar: Optional[List[str]] = None,
        cbar_title: str = None,
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
        legend_padding: The space between legend
        legend_kw: Options to customize legend, will be applied to all,
        cbar_kw: Options to customize colorbar, if categorical cbar, use legend_kw
        heat_cmap: The colormap for heatmap, default: "RdBu_r"
        categorical_cbar: Turn the colorbar in to categorical legend in text
        cbar_title: Set the title for colorbar
        **kwargs: Pass to `seaborn.clustermap <https://seaborn.pydata.org/generated/seaborn.clustermap.html#seaborn.clustermap>`_

    Returns:
        A `seaborn.matrix.ClusterGrid` instance

    """
    row_colors_cmap = "tab20" if row_colors_cmap is None else row_colors_cmap
    col_colors_cmap = "echarts" if col_colors_cmap is None else col_colors_cmap
    heat_cmap = "RdBu_r" if heat_cmap is None else heat_cmap
    legend_kw = set_default(legend_kw, {})
    cbar_kw = set_default(cbar_kw, {})

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

    # plot row colors legend
    legend_transform = dict(
        bbox_to_anchor=(1.05, 1),
        bbox_transform=g.ax_heatmap.transAxes,
        loc="upper left",
    )

    cbar_transform = dict(
        bbox_to_anchor=(1.05, 0),
        ax=g.ax_heatmap,
        bbox_transform=g.ax_heatmap.transAxes,
        loc="lower left",
    )

    legend_options = dict(
        handle="square",
        title_align="left",
    )
    legend_options = {**legend_options, **legend_kw}

    compose_legends = []
    # plot col colors legend
    if col_colors is not None:
        if col_legend_split:
            legend_list = []
            for k, labels in col_legend_contents.items():
                leg = CatLegend(
                    colors=[col_colors_mapper[i] for i in labels],
                    labels=labels,
                    title=k,
                    **legend_options
                )
                legend_list.append(leg)
            g.col_color_legend = hstack(legend_list, spacing=legend_padding)
        else:
            title = col_colors[0] if col_legend_title is None else col_legend_title
            labels, colors = zip(*col_colors_mapper.items())
            g.col_color_legend = CatLegend(colors, labels, ax=g.ax_heatmap, title=title, **legend_options)
        compose_legends.append(g.col_color_legend)

    if row_colors is not None:
        if row_legend_split:
            legend_list = []
            for k, labels in row_legend_contents.items():
                leg = CatLegend(
                    colors=[row_colors_mapper[i] for i in labels],
                    labels=labels,
                    title=k,
                    **legend_options
                )
                legend_list.append(leg)
            g.row_color_legend = hstack(legend_list, spacing=legend_padding)
        else:
            title = row_colors[0] if row_legend_title is None else row_legend_title
            labels, colors = zip(*row_colors_mapper.items())
            g.row_color_legend = CatLegend(colors, labels, title=title, title_align="left")
        compose_legends.append(g.row_color_legend)

    if categorical_cbar is not None:
        cmap = cm.get_cmap(heat_cmap)
        cmap_size = np.linspace(0, cmap.N, len(categorical_cbar), dtype=int)
        labels, colors = categorical_cbar, [cmap(i) for i in cmap_size]
        g.cbar = CatLegend(colors, labels, title=cbar_title, **cbar_transform, **legend_options)
        compose_legends.append(g.cbar)
    else:
        cdata = g.data2d.to_numpy()
        cmin = np.nanmin(cdata)
        cmax = np.nanmax(cdata)
        cbar_options = dict(
            orientation="horizontal",
            title_align="left",
        )
        cbar_options = {**cbar_options, **cbar_kw}
        g.cbar = Colorbar(vmin=cmin, vmax=cmax, cmap=heat_cmap, title=cbar_title, **cbar_transform, **cbar_options)

    g.compose_legends = vstack(compose_legends, padding=0, spacing=legend_padding, align="left", **legend_transform)
    g.ax_heatmap.add_artist(g.compose_legends)

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
