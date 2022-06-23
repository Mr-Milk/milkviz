from __future__ import annotations

from typing import List, Tuple, Any, Dict

import matplotlib as mpl
import matplotlib.axes
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import PatchCollection, LineCollection
from mpl_toolkits.mplot3d import Axes3D

from legendkit import CatLegend, Colorbar
from milkviz.utils import set_ticks, set_spines, \
    color_mapper_cat, rotate_points, color_mapper_val, doc, create_cmap, normalize, \
    set_default


def _init_canvas(ax):
    """For map function only, clear all axis"""
    set_ticks(ax)
    ax.set_aspect("equal")
    ax.set_xticklabels([])
    ax.set_yticklabels([])


def _set_cat_legend(cmapper, ax, legend_kw):
    labels, colors = zip(*cmapper.items())
    legend_options = dict(
        handle="circle",
        bbox_to_anchor=(1.05, 0.5),
        bbox_transform=ax.transAxes,
        loc="center left",
        title_align="left",
    )
    legend_options = {**legend_options, **legend_kw}
    CatLegend(colors, labels, ax=ax, **legend_options)


def _set_cbar(values, cmap, ax, cbar_kw):
    cmin = np.nanmin(values)
    cmax = np.nanmax(values)
    cbar_options = dict(
        bbox_to_anchor=(1.05, 0.5),
        bbox_transform=ax.transAxes,
        loc="center left",
        title_align="left",
    )
    cbar_options = {**cbar_options, **cbar_kw}
    Colorbar(vmin=cmin, vmax=cmax, cmap=cmap, ax=ax, **cbar_options)


@doc
def point_map(
        x,
        y,
        types: List | np.ndarray = None,
        types_colors: Dict = None,
        values: List | np.ndarray = None,
        links: List | np.ndarray = None,
        vmin: float = None,
        vmax: float = None,
        colors: List = None,
        cmap: Any = None,
        rotate: int = None,
        markersize: int = 5,
        linecolor: Any = "#cccccc",
        linewidth: int = 1,
        no_spines: bool = True,
        legend: bool = True,
        legend_kw: Dict = None,
        cbar_kw: Dict = None,
        ax: mpl.axes.Axes = None,
):
    """Point map

    Args:
        x: The x-coord array
        y: The y-coord array
        types: [types] of points
        types_colors: A dictionary that tells color for every type, key is the type and value is the color
        values: [values] of points
        vmin, vmax: [vminmax]
        links: The links between points, should be a list of (point_index_1, point_index_2)
        colors: [hue]
        cmap: [cmap]
        rotate: The degree to rotate the whole plot according to origin
        markersize: The size of marker
        linecolor: The color of lines
        linewidth: The width of lines
        no_spines: [no_spines]
        legend: [legend]
        legend_kw: [legend_kw]
        cbar_kw: [cbar_kw]
        ax: [ax]

    Returns:
        [return_obj]

    """
    if ax is None:
        ax = plt.gca()
    if no_spines:
        set_spines(ax)
    legend_kw = set_default(legend_kw, {})
    cbar_kw = set_default(cbar_kw, {})

    _init_canvas(ax)

    if rotate is not None:
        x, y = rotate_points(x, y, (0, 0), rotate)

    if links is not None:
        if not isinstance(linecolor, str):
            if len(linecolor) != len(links):
                raise ValueError("Length of linecolor must match to links")
        lines = np.array([[[x[i1], y[i1]], [x[i2], y[i2]]] for i1, i2 in links])
        line_collections = LineCollection(lines, linewidths=linewidth, edgecolors=linecolor, zorder=-100)
        ax.add_collection(line_collections)

    if types is not None:
        cmap = set_default(cmap, "echarts")
        cmapper = types_colors
        color_array = None if cmapper is None else [cmapper[t] for t in types]
        if cmapper is None:
            if colors is not None:
                cmapper = color_mapper_cat(types, c_array=colors)
            else:
                cmapper = color_mapper_cat(types, cmap=cmap)
            color_array = [cmapper[t] for t in types]

        ax.scatter(x=x, y=y, c=color_array, s=markersize)
        if legend:
            _set_cat_legend(cmapper, ax, legend_kw)
    else:
        if values is not None:
            cmap = set_default(cmap, "OrRd")
            values = normalize(values, vmin=vmin, vmax=vmax)
            if colors is not None:
                vc_mapper = dict(zip(values, colors))
                cmap = create_cmap([vc_mapper[v] for v in sorted(values)])
            ax.scatter(x=x, y=y, c=values, s=markersize, cmap=cmap)
            if legend:
                _set_cbar(values, cmap, ax, cbar_kw)
        else:
            ax.scatter(x=x, y=y, s=markersize)

    return ax


@doc
def point_map3d(
        x,
        y,
        z,
        types: List | np.ndarray = None,
        types_colors: Dict = None,
        values: List | np.ndarray = None,
        vmin: float = None,
        vmax: float = None,
        colors: List | np.ndarray = None,
        cmap: Any = None,
        legend: bool = True,
        legend_kw: Dict = None,
        cbar_kw: Dict = None,
        markersize: int = 5,
        ax: mpl.axes.Axes = None,
):
    """Point map in 3D

        Args:
            x: The x-coord array
            y: The y-coord array
            z: The z-coord array
            types: [types] of points
            types_colors: A dictionary that tells color for every type, key is the type and value is the color
            values: [values] of points
            vmin, vmax: [vminmax]
            colors: [hue]
            cmap: [cmap]
            legend: [legend]
            legend_kw: [legend_kw]
            cbar_kw: [cbar_kw]
            markersize: The size of marker
            ax: [ax]

        Returns:
            [return_obj]

        """
    legend_kw = set_default(legend_kw, {})
    cbar_kw = set_default(cbar_kw, {})

    if ax is None:
        fig = plt.gcf()
        ax = fig.add_subplot(projection='3d')
    else:
        if not isinstance(ax, Axes3D):
            raise TypeError(f"If you want to use your own axes, initialize it as 3D")
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_zticklabels([])
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    if types is not None:
        cmap = set_default(cmap, "tab20")
        cmapper = types_colors
        color_array = None if cmapper is None else [cmapper[t] for t in types]
        if cmapper is None:
            if colors is not None:
                cmapper = color_mapper_cat(types, c_array=colors)
            else:
                cmapper = color_mapper_cat(types, cmap=cmap)
            color_array = [cmapper[t] for t in types]

        ax.scatter(x, y, z, c=color_array, s=markersize)
        if legend:
            # bbox: 1.2, -0.1
            _set_cat_legend(cmapper, ax, legend_kw)
    else:
        if values is not None:
            cmap = set_default(cmap, "OrRd")
            values = normalize(values, vmin, vmax)
            if colors is not None:
                vc_mapper = dict(zip(values, colors))
                cmap = create_cmap([vc_mapper[v] for v in sorted(values)])
            p = ax.scatter(x, y, z, c=values, s=markersize, cmap=cmap)
            if legend:
                # pos: 1.2, 0.05
                _set_cbar(values, cmap, ax, cbar_kw)
        else:
            ax.scatter(x, y, z, s=markersize)

    return ax


@doc
def polygon_map(
        polygons: List[List[Tuple[float, float]]],
        types: List | np.ndarray = None,
        values: List | np.ndarray = None,
        vmin: float = None,
        vmax: float = None,
        colors: List = None,
        cmap: Any = None,
        legend: bool = True,
        legend_kw: Dict = None,
        cbar_kw: Dict = None,
        rotate: int = None,
        no_spines: bool = True,
        ax: mpl.axes.Axes = None,
):
    """Polygon map

    Args:
        polygons: A list of polygons, a polygon is represented by a list of points
        types: [types] of polygons
        values: [values] of polygons
        vmin, vmax: [vminmax]
        colors: [hue]
        cmap: [cmap]
        legend: [legend]
        legend_kw: [legend_kw]
        cbar_kw: [cbar_kw]
        rotate: The degree to rotate the whole plot according to origin
        no_spines: [no_spines]
        ax: [ax]

    Returns:
        [return_obj]

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
    if no_spines:
        set_spines(ax)

    _init_canvas(ax)

    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)

    if types is not None:
        cmap = set_default(cmap, "tab20")
        if colors is not None:
            cmapper = color_mapper_cat(types, c_array=colors)
        else:
            cmapper = color_mapper_cat(types, cmap=cmap)
        patches = [mpatches.Polygon(polygon) for polygon in polygons]
        patches_collections = PatchCollection(patches, facecolors=[cmapper[t] for t in types])
        ax.add_collection(patches_collections)
        if legend:
            _set_cat_legend(cmapper, ax, legend_kw)
    else:
        if values is not None:
            cmap = set_default(cmap, "OrRd")
            values = normalize(values, vmin, vmax)
            if colors is not None:
                vc_mapper = dict(zip(values, colors))
                cmap = create_cmap([vc_mapper[v] for v in sorted(values)])
            colors = color_mapper_val(values, cmap=cmap)
            patches = [mpatches.Polygon(polygon, color=c) for polygon, c in zip(polygons, colors)]
            patches_collections = PatchCollection(patches, facecolors=colors, cmap=cmap)
            ax.add_collection(patches_collections)
            if legend:
                _set_cbar(values, cmap, ax, cbar_kw)
        else:
            patches = [mpatches.Polygon(polygon) for polygon in polygons]
            patches_collections = PatchCollection(patches)
            ax.add_collection(patches_collections)

    return ax
