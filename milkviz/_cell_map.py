from typing import List, Tuple, Optional, Union, Any, Dict

import matplotlib as mpl
import matplotlib.axes
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.collections import PatchCollection, LineCollection
from matplotlib.colors import Colormap
from natsort import natsorted

from milkviz.utils import set_cbar, set_ticks, set_spines, \
    color_mapper_cat, rotate_points, set_category_legend, color_mapper_val, doc, create_cmap, normalize


@doc
def point_map(
        x: Union[List[float], np.ndarray],
        y: Union[List[float], np.ndarray],
        types: Union[List[str], np.ndarray, None] = None,
        types_colors: Optional[Dict[str, str]] = None,
        values: Union[List[float], np.ndarray, None] = None,
        links: Union[List[Tuple[int, int]], np.ndarray, None] = None,
        vmin: Optional[float] = None,
        vmax: Optional[float] = None,
        colors: Optional[List[Any]] = None,
        cmap: Union[str, Colormap] = None,
        legend_title: Optional[str] = None,
        rotate: Optional[int] = None,
        markersize: Optional[int] = 5,
        linecolor: Union[str, List[str]] = "#cccccc",
        linewidth: int = 1,
        no_spines: bool = True,
        ax: Optional[mpl.axes.Axes] = None,
):
    """Point map

    Args:
        x: The x-coord array
        y: The y-coord array
        types: [types] of points
        types_colors: A dictionary that tells color for every type, key is the type and value is the color
        values: [values] of points
        links: The links between points, should be a list of (point_index_1, point_index_2)
        colors: [hue]
        cmap: [cmap]
        legend_title: [legend_title]
        rotate: The degree to rotate the whole plot according to origin
        markersize: The size of marker
        linecolor: The color of lines
        linewidth: The width of lines
        no_spines: [no_spines]
        ax: [ax]

    Returns:
        [return_obj]

    """
    if ax is None:
        ax = plt.gca()
    if no_spines:
        set_spines(ax)
    set_ticks(ax)
    ax.set_aspect("equal")
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    if rotate is not None:
        x, y = rotate_points(x, y, (0, 0), rotate)

    if links is not None:
        if not isinstance(linecolor, str):
            if len(linecolor) != len(links):
                raise ValueError("Length of linecolor must match to links")
        lines = [[(x[i1], y[i1]), (x[i2], y[i2])] for i1, i2 in links]
        line_collections = LineCollection(lines, linewidths=linewidth, edgecolors=linecolor, zorder=-100)
        ax.add_collection(line_collections)

    if types is not None:
        cmap = "tab20" if cmap is None else cmap
        legend_title = "type" if legend_title is None else legend_title
        cmapper = types_colors
        color_array = None if cmapper is None else [cmapper[t] for t in types]
        if cmapper is None:
            if colors is not None:
                cmapper = color_mapper_cat(types, c_array=colors)
            else:
                cmapper = color_mapper_cat(types, cmap=cmap)
            color_array = [cmapper[t] for t in types]

        ax.scatter(x=x, y=y, c=color_array, s=markersize)
        set_category_legend(ax, cmapper, (1.05, 0, 1, 1), legend_title)
    else:
        if values is not None:
            cmap = "OrRd" if cmap is None else cmap
            legend_title = "value" if legend_title is None else legend_title
            values = normalize(values, vmin, vmax)
            if colors is not None:
                vc_mapper = dict(zip(values, colors))
                cmap = create_cmap([vc_mapper[v] for v in sorted(values)])
            p = ax.scatter(x=x, y=y, c=values, s=markersize, cmap=cmap)
            cmin = np.nanmin(values)
            cmax = np.nanmax(values)
            set_cbar(ax, p, (1.07, 0, 0.1, 0.3), legend_title, cmin, cmax)
        else:
            ax.scatter(x=x, y=y, s=markersize)

    return ax


def point_map3d(
        x: Union[List[float], np.ndarray],
        y: Union[List[float], np.ndarray],
        z: Union[List[float], np.ndarray],
        types: Union[List[str], np.ndarray, None] = None,
        types_colors: Optional[Dict[str, str]] = None,
        values: Union[List[float], np.ndarray, None] = None,
        vmin: Optional[float] = None,
        vmax: Optional[float] = None,
        colors: Optional[List[Any]] = None,
        cmap: Union[str, Colormap] = None,
        legend_title: Optional[str] = None,
        markersize: Optional[int] = 5,
        ax: Optional[mpl.axes.Axes] = None,
):
    """Point map in 3D

        Args:
            x: The x-coord array
            y: The y-coord array
            z: The z-coord array
            types: [types] of points
            types_colors: A dictionary that tells color for every type, key is the type and value is the color
            values: [values] of points
            colors: [hue]
            cmap: [cmap]
            legend_title: [legend_title]
            markersize: The size of marker
            ax: [ax]

        Returns:
            [return_obj]

        """
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
        cmap = "tab20" if cmap is None else cmap
        legend_title = "type" if legend_title is None else legend_title
        cmapper = types_colors
        color_array = None if cmapper is None else [cmapper[t] for t in types]
        if cmapper is None:
            if colors is not None:
                cmapper = color_mapper_cat(types, c_array=colors)
            else:
                cmapper = color_mapper_cat(types, cmap=cmap)
            color_array = [cmapper[t] for t in types]

        ax.scatter(x, y, z, c=color_array, s=markersize)
        set_category_legend(ax, cmapper, (1.2, -0.1, 1, 1), legend_title)
    else:
        if values is not None:
            cmap = "OrRd" if cmap is None else cmap
            legend_title = "value" if legend_title is None else legend_title
            values = normalize(values, vmin, vmax)
            if colors is not None:
                vc_mapper = dict(zip(values, colors))
                cmap = create_cmap([vc_mapper[v] for v in sorted(values)])
            p = ax.scatter(x, y, z, c=values, s=markersize, cmap=cmap)
            cmin = np.nanmin(values)
            cmax = np.nanmax(values)
            set_cbar(ax, p, (1.2, 0.05, 0.1, 0.3), legend_title, cmin, cmax)
        else:
            ax.scatter(x, y, z, s=markersize)

    return ax





@doc
def polygon_map(
        polygons: List[List[Tuple[float, float]]],
        types: Union[List[str], np.ndarray, None] = None,
        values: Union[List[float], np.ndarray, None] = None,
        colors: Optional[List[Any]] = None,
        cmap: Union[str, Colormap] = None,
        legend_title: Optional[str] = None,
        rotate: Optional[int] = None,
        no_spines: bool = True,
        ax: Optional[mpl.axes.Axes] = None,
):
    """Polygon map

    Args:
        polygons: A list of polygons, a polygon is represented by a list of points
        types: [types] of polygons
        values: [values] of polygons
        colors: [hue]
        cmap: [cmap]
        legend_title: [legend_title]
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
    set_ticks(ax)
    ax.set_aspect("equal")
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)

    if types is not None:
        cmap = "tab20" if cmap is None else cmap
        legend_title = "type" if legend_title is None else legend_title
        uni_types = natsorted(np.unique(types))
        cmapper, color_array = None, None
        if colors is not None:
            cmapper = color_mapper_cat(types, c_array=colors)
            color_array = colors
        else:
            cmapper = color_mapper_cat(types, cmap=cmap)
            color_array = [cmapper[t] for t in types]
        patches = [mpatches.Polygon(polygon) for polygon in polygons]
        patches_collections = PatchCollection(patches, facecolors=[cmapper[t] for t in types])
        ax.add_collection(patches_collections)
        set_category_legend(ax, cmapper, (1.05, 0, 1, 1), legend_title)
    else:
        if values is not None:
            cmap = "OrRd" if cmap is None else cmap
            legend_title = "value" if legend_title is None else legend_title
            if colors is not None:
                vc_mapper = dict(zip(values, colors))
                cmap = create_cmap([vc_mapper[v] for v in sorted(values)])
            colors = color_mapper_val(values, cmap=cmap)
            patches = [mpatches.Polygon(polygon, color=c) for polygon, c in zip(polygons, colors)]
            patches_collections = PatchCollection(patches, facecolors=colors, cmap=cmap)
            ax.add_collection(patches_collections)
            cmin = np.nanmin(values)
            cmax = np.nanmax(values)
            set_cbar(ax, patches_collections, (1.07, 0, 0.1, 0.3), legend_title, cmin, cmax)
        else:
            patches = [mpatches.Polygon(polygon) for polygon in polygons]
            patches_collections = PatchCollection(patches)
            ax.add_collection(patches_collections)

    return ax
