from typing import List, Any, Tuple, Optional, Union, Dict

import matplotlib as mpl
import numpy as np
from matplotlib import cm
from matplotlib import pyplot as plt
from matplotlib.axes import Axes

from legendkit import Colorbar
from milkviz.utils import norm_arr, set_spines, doc, set_default


@doc
def graph(
        edges: List[Tuple[Any, Any]],
        nodes: List = None,
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
        node_cbar_kw: Dict = None,
        edge_cbar_kw: Dict = None,
        sizes: Tuple[float, float] = (100, 1500),
        node_shape: str = "o",
        linewidth: Tuple[float, float] = (1, 10),
        connectionstyle: str = 'arc3,rad=0.2',
        layout: str = "kamada_kawai_layout",
        arrowstyle: str = "-",
        ax: Optional[Axes] = None,
) -> Axes:
    """Graph layout

    Args:
        nodes: The graph nodes, a list of nodes
        edges: The graph data, a list of (source, target)
        nodes_size: [size]
        nodes_color: [hue]
        edges_width: The width array that map to edges width
        edges_color: The color array that map to edges color
        nodes_size_range: Use to remap the nodes size, overwrite the min, max of nodes_size array
        nodes_color_range: Use to remap the nodes colors, overwrite the min, max of nodes_color array
        edges_width_range: Use to remap the edges width, overwrite the min, max of nodes_size array
        edges_color_range: Use to remap the edges colors, overwrite the min, max of edges_color array
        node_cmap: The colormap for node
        edge_cmap: The colormap for edge
        node_cbar_kw: To control the cbar of node
        edge_cbar_kw: To control the cbar of edge
        sizes: [sizes]
        node_shape: The shape of the node. Specification is as matplotlib.scatter marker, one of ???so^>v<dph8???.
        linewidth: Line width of symbol border
        connectionstyle: Pass the connectionstyle parameter to create curved arc of rounding
            radius rad. For example, connectionstyle='arc3,rad=0.2'.
            See `matplotlib.patches.ConnectionStyle <https://matplotlib.org/stable/api/_as_gen/matplotlib.patches.ConnectionStyle.html#matplotlib.patches.ConnectionStyle>`_ and
            `matplotlib.patches.FancyArrowPatch <https://matplotlib.org/stable/api/_as_gen/matplotlib.patches.FancyArrowPatch.html#matplotlib.patches.FancyArrowPatch>`_ for more info.
        layout: See
            `networkx.drawing.layout <https://networkx.org/documentation/stable/reference/drawing.html#module-networkx.drawing.layout>`_
        arrowstyle: For directed graphs and arrows==True defaults to ???-|>???, See
            `matplotlib.patches.ArrowStyle <https://matplotlib.org/stable/api/_as_gen/matplotlib.patches.ArrowStyle.html#matplotlib.patches.ArrowStyle>`_ for more options.
        ax: [ax]

    Returns:
        [return_obj]

    """
    try:
        import networkx as nx
    except ImportError:
        raise ImportError("Extra dependencies needed, Try `pip install networkx`")

    node_cbar_kw = set_default(node_cbar_kw, {})
    edge_cbar_kw = set_default(edge_cbar_kw, {})

    G = nx.Graph()
    G.add_edges_from(edges)
    if nodes is not None:
        G.add_nodes_from(nodes)
    if ax is None:
        ax = plt.gca()

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
                                           arrowstyle=arrowstyle,
                                           connectionstyle=connectionstyle,
                                           # for safety
                                           node_size=nodes_size,
                                           node_shape=node_shape,
                                           )
    label_options = {"ec": "k", "fc": "white", "alpha": 0.7}
    nx.draw_networkx_labels(G, pos, font_size=mpl.rcParams['font.size'], bbox=label_options)

    if node_cmin is not None:
        node_cbar_options = dict(
            orientation="horizontal",
            bbox_to_anchor=(1, -0.05),
            bbox_transform=ax.transAxes,
            loc="upper right",
            title_align="left",
        )
        node_cbar_options = {**node_cbar_options, **node_cbar_kw}
        Colorbar(vmin=node_cmin, vmax=node_cmax, ax=ax, cmap=node_cmap, **node_cbar_options)

    if edge_cmin is not None:
        edge_cbar_options = dict(
            bbox_to_anchor=(1.05, 0),
            bbox_transform=ax.transAxes,
            loc="lower left",
            title_align="left",
        )
        edge_cbar_options = {**edge_cbar_options, **edge_cbar_kw}
        Colorbar(vmin=edge_cmin, vmax=edge_cmax, ax=ax, cmap=edge_cmap, **edge_cbar_options)
    set_spines(ax)
    return ax
