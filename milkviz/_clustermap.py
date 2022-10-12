from __future__ import annotations

import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.collections import QuadMesh
from matplotlib.colors import to_hex
from typing import List, Optional, Dict, Any

from legendkit import CatLegend, Colorbar, vstack, hstack
from milkviz.utils import set_default, cat_colors, get_colormap


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
        row_cluster=True,
        col_cluster=True,
        **kwargs,
) -> sns.matrix.ClusterGrid:
    """Color or label annotated clustermap

    Parameters
    ----------
    data : pd.DataFrame
        A dataframe, multi-levels annotations should store in MultiIndex
    row_label : str, array-like of str
        The index level used for y-axis label
    col_label : str, array-like of str
        The columns level used for x-axis label
    row_colors : str, array-like of str
        The index levels used to label in color stripe
    col_colors : str, array-like of str
        The columns levels used to label in color stripe
    row_colors_cmap : default: "tab20"
        The colormap for row_colors
    col_colors_cmap : default: "echarts"
        The colormap for col_colors
    row_colors_order : dict
        Reorder the items in each level
    col_colors_order : dict
    row_colors_label : dict
        Overwrite the name of each level,
    col_colors_label : dict
    row_legend_split : bool, default: True
        Whether to split each level of colors stripe
    col_legend_split : bool, default: True
    row_legend_title : str
        The title of row legend, when row_legend_split = False
    col_legend_title : str
        The title of col legend, when col_legend_split = False
    legend_padding : float
        The space between legend
    legend_kw : dict
        Options to customize legend, will be applied to all,
    cbar_kw : dict
        Options to customize colorbar, if categorical cbar, use legend_kw
    heat_cmap : default: "RdBu_r"
        The colormap for heatmap
    categorical_cbar : array-like
        Turn the colorbar in to categorical legend in text
    cbar_title : str
        Set the title for colorbar
    row_cluster : bool
    col_cluster : bool
    kwargs :
        Pass to :func:`seaborn.clustermap`


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
        row_legend_contents = \
            {rc: info[rc].unique().flatten() for rc in row_colors}
        color_array, legend_labels, legend_colors = \
            cat_colors(info.to_numpy().flatten(), cmap=row_colors_cmap)
        # convert to hex to ensure str dtype
        hex_colors = [to_hex(c) for c in legend_colors]
        row_colors_mapper = dict(zip(legend_labels, hex_colors))
        clustermap_kwargs["row_colors"] = info.replace(row_colors_mapper)

    if col_colors is not None:
        info = col_info[col_colors]
        col_legend_contents = \
            {cc: info[cc].unique().flatten() for cc in col_colors}
        color_array, legend_labels, legend_colors = \
            cat_colors(info.to_numpy().flatten(), cmap=col_colors_cmap)
        hex_colors = [to_hex(c) for c in legend_colors]
        col_colors_mapper = dict(zip(legend_labels, hex_colors))
        clustermap_kwargs["col_colors"] = info.replace(col_colors_mapper)

    g = sns.clustermap(plot_data,
                       col_cluster=col_cluster,
                       row_cluster=row_cluster,
                       **clustermap_kwargs)

    # plot row colors legend
    legend_options = dict(
        handle="square",
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
            title = col_colors[
                0] if col_legend_title is None else col_legend_title
            labels, colors = zip(*col_colors_mapper.items())
            g.col_color_legend = CatLegend(ax=g.ax_heatmap,
                                           colors=colors,
                                           labels=labels,
                                           title=title,
                                           **legend_options)
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
            title = row_colors[
                0] if row_legend_title is None else row_legend_title
            labels, colors = zip(*row_colors_mapper.items())
            g.row_color_legend = CatLegend(ax=g.ax_heatmap,
                                           colors=colors,
                                           labels=labels,
                                           title=title,
                                           **legend_options)
        compose_legends.append(g.row_color_legend)

    if categorical_cbar is not None:
        cmap = get_colormap(heat_cmap)
        cmap_size = np.linspace(0, cmap.N, len(categorical_cbar), dtype=int)
        labels, colors = categorical_cbar, [cmap(i) for i in cmap_size]
        g.cbar = CatLegend(ax=g.ax_heatmap,
                           colors=colors, labels=labels,
                           title=cbar_title, **legend_options)
        compose_legends.append(g.cbar)
    else:
        cbar_options = dict(
            title=cbar_title,
            orientation="horizontal",
            loc="out lower right",
            ticklocation="bottom",
        )
        cbar_options = {**cbar_options, **cbar_kw}

        mesh = None
        for i in g.ax_heatmap.get_children():
            if isinstance(i, QuadMesh):
                mesh = i
        g.cbar = Colorbar(mesh, **cbar_options)

    g.compose_legends = vstack(compose_legends, padding=0,
                               ax=g.ax_heatmap,
                               spacing=legend_padding, align="left",
                               loc="out right upper"
                               )
    g.ax_heatmap.legend_ = g.compose_legends

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

    if not row_cluster:
        g.ax_row_dendrogram.remove()
    if not col_cluster:
        g.ax_col_dendrogram.remove()

    return g
