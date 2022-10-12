import matplotlib as mpl
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.colors import Normalize
from seaborn import despine

from legendkit import Colorbar
from milkviz.utils import set_default, get_colormap


def graph(
        edges,
        nodes=None,
        nodes_size=None,
        nodes_color="#69B0AC",
        edges_width=None,
        edges_color="#F7C242",
        nodes_size_range=None,
        nodes_color_range=None,
        edges_width_range=None,
        edges_color_range=None,
        node_cmap="Purples",
        edge_cmap="RdBu",
        node_cbar_kw=None,
        edge_cbar_kw=None,
        node_shape="o",
        sizes=(100, 1500),
        linewidth=(1, 10),
        connectionstyle='arc3,rad=0.2',
        layout="kamada_kawai_layout",
        arrowstyle="-",
        ax=None,
) -> Axes:
    """Graph layout

    Parameters
    ----------
    nodes : array-like
        The graph nodes, a list of nodes
    edges : array-like
        The graph data, a list of (source, target)
    nodes_size : array-like
        The size of nodes
    nodes_color :
        The color of nodes
    edges_width :
        The width array that map to edge width
    edges_color :
        The color array that map to edges color
    nodes_size_range :
        Use to remap the nodes size,
        overwrite the min, max of nodes_size array
    nodes_color_range :
        Use to remap the nodes colors,
        overwrite the min, max of nodes_color array
    edges_width_range :
        Use to remap the edges' width,
        overwrite the min, max of edges_size array
    edges_color_range :
        Use to remap the edges colors,
        overwrite the min, max of edges_color array
    node_cmap :
        The colormap for node
    edge_cmap :
        The colormap for edge
    node_cbar_kw :
        To control the cbar of node
    edge_cbar_kw :
        To control the cbar of edge
    sizes :
        The range of size
    node_shape :
        The shape of the node, a matplotlib marker.
    linewidth :
        Line width of symbol border
    connectionstyle :
        Pass the connectionstyle parameter to create curved arc of rounding
        radius rad. For example, connectionstyle='arc3,rad=0.2'.
        See :class:`matplotlib.patches.ConnectionStyle` and
        :class:`matplotlib.patches.FancyArrowPatch` for more info.
    layout : See
        :func:`networkx.drawing.layout`
    arrowstyle : For directed graphs and arrows==True defaults to ‘-|>’, See
        :class:`matplotlib.patches.ArrowStyle` for more options.
    ax :

    """
    try:
        import networkx as nx
    except ImportError:
        raise ImportError("Try `pip install networkx`")

    node_cbar_kw = set_default(node_cbar_kw, {})
    edge_cbar_kw = set_default(edge_cbar_kw, {})

    G = nx.Graph()
    G.add_edges_from(edges)
    if nodes is not None:
        G.add_nodes_from(nodes)
    if ax is None:
        ax = plt.gca()

    if layout == "bipartite_layout":
        pos = getattr(nx.drawing.layout, layout
                      ).__call__(G, [e[0] for e in edges])
    else:
        pos = getattr(nx.drawing.layout, layout).__call__(G)

    if nodes_size is not None:
        node_size_norm = Normalize()
        if nodes_size_range is not None:
            vmin, vmax = nodes_size_range
            node_size_norm.vmin = vmin
            node_size_norm.vmax = vmax
        else:
            node_size_norm.autoscale(nodes_size)
        nodes_size = node_size_norm(
            nodes_size) * (sizes[1] - sizes[0]) + sizes[0]
    else:
        nodes_size = sizes[0]

    if edges_width is not None:

        if edges_width_range is not None:
            vmin, vmax = edges_width_range
            edges_width_norm = Normalize(vmin=vmin, vmax=vmax)
        else:
            edges_width_norm = Normalize()
            edges_width_norm.autoscale(edges_width)
        edges_width = edges_width_norm(
            edges_width) * (linewidth[1] - linewidth[0]) + linewidth[0]
    else:
        edges_width = linewidth[0]

    node_cmin, node_cmax = None, None
    edge_cmin, edge_cmax = None, None
    if nodes_color is not None:
        if not isinstance(nodes_color, str):
            if nodes_color_range is None:
                node_cmin, node_cmax = (np.nanmin(nodes_color),
                                        np.nanmax(nodes_color))
            else:
                node_cmin, node_cmax = nodes_color_range

    if edges_color is not None:
        if not isinstance(edges_color, str):
            if edges_color_range is None:
                edge_cmin, edge_cmax = (np.nanmin(edges_color),
                                        np.nanmax(edges_color))
            else:
                edge_cmin, edge_cmax = edges_color_range
    nodes_patches = nx.draw_networkx_nodes(G, pos,
                                           node_size=nodes_size,
                                           node_color=nodes_color,
                                           node_shape=node_shape,
                                           vmin=node_cmin,
                                           vmax=node_cmax,
                                           cmap=get_colormap(node_cmap),
                                           linewidths=0,
                                           )
    edges_patches = nx.draw_networkx_edges(G, pos,
                                           width=edges_width,
                                           edge_color=edges_color,
                                           edge_vmin=edge_cmin,
                                           edge_vmax=edge_cmax,
                                           edge_cmap=get_colormap(edge_cmap),
                                           arrowstyle=arrowstyle,
                                           connectionstyle=connectionstyle,
                                           )
    label_options = {"ec": "k", "fc": "white", "alpha": 0.7}
    nx.draw_networkx_labels(G, pos,
                            font_size=mpl.rcParams['font.size'],
                            bbox=label_options)

    if node_cmin is not None:
        node_cbar_options = dict(
            orientation="horizontal",
            loc="out lower right", )
        node_cbar_options = {**node_cbar_options, **node_cbar_kw}
        Colorbar(nodes_patches, ax=ax, **node_cbar_options)

    if edge_cmin is not None:
        edge_cbar_options = dict(
            loc="out right lower",
        )
        edge_cbar_options = {**edge_cbar_options, **edge_cbar_kw}
        Colorbar(edges_patches, ax=ax, **edge_cbar_options)
    despine(ax=ax, left=True, bottom=True)
    return ax
