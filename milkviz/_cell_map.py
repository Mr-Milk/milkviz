import matplotlib as mpl
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.collections import PatchCollection, LineCollection
from matplotlib.colors import is_color_like, Normalize, TwoSlopeNorm
from mpl_toolkits.mplot3d import Axes3D

from legendkit import Colorbar
from .utils import rotate_points, set_default, cat_colors, set_cat_legend


def _set_cbar(mappable, ax, cbar_kw):
    cbar_options = dict(
        loc="out right center",
    )
    cbar_options = {**cbar_options, **cbar_kw}
    cb = Colorbar(mappable=mappable, ax=ax, **cbar_options)
    cb.ax.tick_params(left=True, right=True)


def handle_cmap_norm(cmap, norm, values, vmin, vmax, center):
    cmap = set_default(cmap, "OrRd")
    vmin = np.nanmin(values) if vmin is None else vmin
    vmax = np.nanmax(values) if vmax is None else vmax
    if center is not None:
        norm = TwoSlopeNorm(center, vmin=vmin, vmax=vmax)
    else:
        if norm is None:
            norm = Normalize(vmin=vmin, vmax=vmax)
    return cmap, norm


def point_map(
        points,
        *,
        types=None,
        order=None,
        values=None,
        links=None,
        colors=None,
        cmap=None,
        norm=None,
        vmin=None,
        vmax=None,
        center=None,
        rotate=None,
        markersize=5,
        edgecolor=None,
        edgewidth=None,
        linkcolor="#cccccc",
        linkwidth=1,
        frameon=False,
        legend=True,
        legend_kw=None,
        cbar_kw=None,
        ax=None,
        **kwargs,
):
    """Point map

    Parameters
    ----------
    points : array-like
        2D or 3D points
    types : array-like
        The categorical label for each point
    order : array-like
        The order of types that presents in legends
    values : array-like
        The numeric value for each point
    links : array-like of (point_index1, point_index2)
        The links between points
    colors : array, mapping
        Either array that represents colors or a dict that map types to colors
    cmap :
    norm :
    vmin :
    vmax :
    center :
    rotate : float
        The degree to rotate the whole plot according to origin,
        only rotate x and y
    markersize : float
        The size of marker
    edgecolor : color
    edgewidth : float
    linkcolor :
        The color of lines
    linkwidth :
        The width of lines
    frameon : bool
        If True, will turn off the frame of the plot
    legend : bool
        Whether to show the legend
    legend_kw : dict
        Pass to :func:`legendkit.legend`
    cbar_kw : dict
        Pass to :func:`legend.colorbar`
    ax : Axes
    kwargs :
        Pass to :func:`matplotlib.axes.Axes.scatter`

    Returns
    -------
    Axes

    """
    size, dim = np.asarray(points).shape
    x = points[:, 0]
    y = points[:, 1]
    z = None
    if dim == 3:
        z = points[:, 2]
        if ax is None:
            fig = plt.gcf()
            ax = fig.add_subplot(projection='3d')
        else:
            if not isinstance(ax, Axes3D):
                raise TypeError(f"If you want to use your own axes, "
                                f"initialize it as 3D")
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.set_zticklabels([])
        ax.set_xlabel("X", labelpad=-14)
        ax.set_ylabel("Y", labelpad=-14)
        ax.set_zlabel("Z", labelpad=-14)
    else:
        ax = plt.gca()
        ax.set_aspect("equal")
        if frameon:
            ax.tick_params(top=False, bottom=False, left=False, right=False,
                           labeltop=False, labelbottom=False,
                           labelleft=False, labelright=False)
        else:
            ax.set_axis_off()

    legend_kw = set_default(legend_kw, {})
    cbar_kw = set_default(cbar_kw, {})

    if rotate is not None:
        x, y = rotate_points(x, y, (0, 0), rotate)

    points = (x, y) if dim == 2 else (x, y, z)

    if (links is not None) & (dim == 2):
        if not is_color_like(linkcolor):
            if len(linkcolor) != len(links):
                raise ValueError("Length of linecolor must match to links")
        lines = np.array([[[x[i1], y[i1]],
                           [x[i2], y[i2]]] for i1, i2 in links])
        line_collections = LineCollection(lines, linewidths=linkwidth,
                                          edgecolors=linkcolor, zorder=-100)
        ax.add_collection(line_collections)

    if types is not None:
        color_array, legend_labels, legend_colors = \
            cat_colors(types, order, cmap, colors)
        ax.scatter(*points, s=markersize, c=color_array,
                   linewidths=edgewidth,
                   edgecolors=edgecolor,
                   **kwargs)
        if legend:
            set_cat_legend(legend_labels, legend_colors, ax,
                           edgecolor=edgecolor,
                           edgewidth=edgewidth,
                           legend_kw=legend_kw)
    else:
        if values is not None:
            cmap, norm = handle_cmap_norm(cmap, norm, values,
                                          vmin, vmax, center)
            mappable = ax.scatter(*points, c=values, s=markersize,
                                  norm=norm, cmap=cmap,
                                  linewidths=edgewidth,
                                  edgecolors=edgecolor,
                                  **kwargs)
            if legend:
                _set_cbar(mappable, ax, cbar_kw)
        else:
            ax.scatter(*points, s=markersize, **kwargs)
    return ax


def polygon_map(
        polygons,
        *,
        types=None,
        order=None,
        values=None,
        colors=None,
        cmap=None,
        norm=None,
        vmin=None,
        vmax=None,
        center=None,
        rotate=None,
        edgecolor=None,
        edgewidth=None,
        frameon=False,
        legend=True,
        legend_kw=None,
        cbar_kw=None,
        ax: mpl.axes.Axes = None,
        **kwargs,
):
    """Polygon map

    Parameters
    ----------
    polygons : array-like
        A list of polygons, a polygon is represented by a list of points
    types :
        The categorical label for each polygon
    order : array-like
        The order of types that presents in legends
    values : array-like
        The numeric value for each polygon
    colors : array, mapping
        Either array that represents colors or a dict that map types to colors
    cmap :
    norm :
    vmin :
    vmax :
    center :
    rotate : float
        The degree to rotate the whole plot according to origin
    edgecolor : color
    edgewidth : float
    frameon : bool
        If True, will turn off the frame of the plot
    legend : bool
        Whether to show the legend
    legend_kw : dict
        Pass to :func:`legendkit.legend`
    cbar_kw : dict
        Pass to :func:`legend.colorbar`
    ax : Axes
    kwargs :
        Pass to :func:`matplotlib.axes.Axes.scatter`

    Returns
    -------
    Axes

    """
    polygons = [np.array(polygon) for polygon in polygons]
    vstack_poly = np.vstack(polygons)
    xmin, ymin = np.min(vstack_poly, axis=0)
    xmax, ymax = np.max(vstack_poly, axis=0)
    legend_kw = set_default(legend_kw, {})
    cbar_kw = set_default(cbar_kw, {})

    if rotate is not None:
        rotated_polygons = []
        for polygon in polygons:
            x, y = rotate_points(polygon[:, 0], polygon[:, 1], (0, 0), rotate)
            rotated_polygons.append([(i, j) for i, j in zip(x, y)])
        polygons = rotated_polygons

    if ax is None:
        ax = plt.gca()
        ax.set_aspect('equal')
    if frameon:
        ax.tick_params(top=False, bottom=False, left=False, right=False,
                       labeltop=False, labelbottom=False,
                       labelleft=False, labelright=False)
    else:
        ax.set_axis_off()

    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)

    patches = [mpatches.Polygon(polygon) for polygon in polygons]

    if types is not None:
        cmap = set_default(cmap, "echarts")
        color_array, legend_labels, legend_colors = \
            cat_colors(types, order, cmap, colors)

        patches_collections = PatchCollection(
            patches,
            facecolors=color_array,
            linewidths=edgewidth,
            edgecolors=edgecolor,
            **kwargs,
        )
        if legend:
            set_cat_legend(legend_labels, legend_colors, ax,
                           shape="square",
                           edgecolor=edgecolor,
                           edgewidth=edgewidth,
                           legend_kw=legend_kw)
    else:
        if values is not None:
            cmap, norm = handle_cmap_norm(cmap, norm, values,
                                          vmin, vmax, center)
            patches_collections = PatchCollection(
                patches, cmap=cmap, norm=norm, linewidths=edgewidth,
                edgecolors=edgecolor, **kwargs)
            patches_collections.set_array(values)
            if legend:
                _set_cbar(patches_collections, ax, cbar_kw)
        else:
            patches_collections = PatchCollection(patches)
    ax.add_collection(patches_collections)

    return ax
