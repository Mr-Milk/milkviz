from typing import List, Any, Tuple, Optional, Union

import matplotlib as mpl
import numpy as np
from matplotlib import cm
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
import networkx as nx

from milkviz.utils import norm_arr, set_spines, set_cbar


def graph(
        edges: List[Tuple[Any, Any]],
        nodes_size: Optional[List[float]] = None,
        nodes_color: Union[List[float], List[str], str, None] = "#69B0AC",
        edges_width: Optional[List[float]] = None,
        edges_color: Union[List[float], List[str], str, None] = "#F7C242",
        nodes_size_range: Optional[Tuple[float, float]] = None,
        nodes_color_range: Optional[Tuple[float, float]] = None,
        edges_width_range: Optional[Tuple[float, float]] = None,
        edges_color_range: Optional[Tuple[float, float]] = None,
        node_cmap: Optional[str] = "Purples",
        edge_cmap: Optional[str] = "RdBu",
        node_color_legend_title: str = "node\ncolor",
        edge_color_legend_title: str = "edge\ncolor",
        sizes: Tuple[float, float] = (100, 1500),
        node_shape: str = "o",
        linewidth: Tuple[float, float] = (1, 10),
        connectionstyle: str = 'arc3,rad=0.2',
        layout: str = "kamada_kawai_layout",
        directed: bool = False,
        ax: Optional[Axes] = None,
) -> Axes:
    G = nx.Graph(edges)
    if ax is None:
        _, ax = plt.subplots()

    if layout == "bipartite_layout":
        pos = getattr(nx.drawing.layout, layout).__call__(G, [e[0] for e in edges])
    else:
        pos = getattr(nx.drawing.layout, layout).__call__(G)

    if nodes_size is not None:
        vmin, vmax = (None, None) if nodes_size_range is None else nodes_size_range
        nodes_size = norm_arr(nodes_size, size=sizes, vmin=vmin, vmax=vmax)
    else:
        nodes_size = sizes[0]

    if edges_width is not None:
        vmin, vmax = (None, None) if edges_width_range is None else edges_width_range
        edges_width = norm_arr(edges_width, size=linewidth, vmin=vmin, vmax=vmax)
    else:
        edges_width = linewidth[0]

    node_cmin, node_cmax = None, None
    edge_cmin, edge_cmax = None, None
    if nodes_color is not None:
        if not isinstance(nodes_color, str):
            if nodes_color_range is None:
                node_cmin, node_cmax = (np.nanmin(nodes_color), np.nanmax(nodes_color))
            else:
                node_cmin, node_cmax = nodes_color_range

    if edges_color is not None:
        if not isinstance(edges_color, str):
            if edges_color_range is None:
                edge_cmin, edge_cmax = (np.nanmin(edges_color), np.nanmax(edges_color))
            else:
                edge_cmin, edge_cmax = edges_color_range
    nodes_patches = nx.draw_networkx_nodes(G, pos,
                                           node_size=nodes_size,
                                           node_color=nodes_color,
                                           node_shape=node_shape,
                                           vmin=node_cmin,
                                           vmax=node_cmax,
                                           cmap=cm.get_cmap(node_cmap),
                                           linewidths=0,
                                           )
    edges_patches = nx.draw_networkx_edges(G, pos,
                                           width=edges_width,
                                           edge_color=edges_color,
                                           edge_vmin=edge_cmin,
                                           edge_vmax=edge_cmax,
                                           edge_cmap=cm.get_cmap(edge_cmap),
                                           connectionstyle=connectionstyle,
                                           # for safety
                                           node_size=nodes_size,
                                           node_shape=node_shape,
                                           )
    label_options = {"ec": "k", "fc": "white", "alpha": 0.7}
    labels = nx.draw_networkx_labels(G, pos, font_size=mpl.rcParams['font.size'], bbox=label_options)

    bbox_loc = {0: (1.07, 0, 0.1, 0.3), 1: (1.27, 0, 0.1, 0.3)}
    cbar_count = 0
    if node_cmin is not None:
        set_cbar(ax, patches=nodes_patches, bbox=bbox_loc[cbar_count], title=node_color_legend_title,
                 cmin=node_cmin, cmax=node_cmax, cmap=node_cmap)
    cbar_count += 1
    if edge_cmin is not None:
        set_cbar(ax, patches=edges_patches, bbox=bbox_loc[cbar_count], title=edge_color_legend_title,
                 cmin=edge_cmin, cmax=edge_cmax, cmap=edge_cmap)
    set_spines(ax)
    plt.tight_layout()
    return ax
