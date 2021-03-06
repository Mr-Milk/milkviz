from typing import Union, List, Any, Optional, Dict

import numpy as np
from matplotlib import cm
from matplotlib import colors as mcolors
from matplotlib.colors import Colormap
from matplotlib.colors import to_hex

Colors = Union[str, List[str], Colormap]


def mask_triu(arr, k=1):
    if not isinstance(arr, np.ndarray):
        arr = np.array(arr, dtype=np.float64)
    arr = arr.astype(np.float64)
    shape = arr.shape
    if shape[0] != shape[1]:
        raise ValueError("Must be a square")
    iu = np.triu_indices(shape[0], k=k)
    arr[iu] = np.nan
    return np.fliplr(arr.T)


def norm_arr(arr, size=(1, 100), vmin=None, vmax=None):
    """Normalize the array to a specific range"""
    if not isinstance(arr, np.ndarray):
        arr = np.array(arr)
    arr = arr.flatten()
    add_count = 0
    if vmin is not None:
        arr = np.array([*arr, vmin])
        add_count += 1
    if vmax is not None:
        arr = np.array([*arr, vmax])
        add_count += 1
    amin = np.nanmin(arr)
    amax = np.nanmax(arr)
    size_range = size[1] - size[0]
    arr = (arr - amin) * (size_range / (amax - amin))
    arr += size[0]
    slice_ = -add_count if add_count > 0 else None
    return arr[:slice_]


def adaptive_figsize(size, min_side=5):
    """scale the min number to min_side, while maintain the ratio"""
    size = np.array(size, dtype=np.float64)
    amin = np.amin(size)
    min_ix = np.argmin(size)
    scale = min_side / amin
    if amin < min_side:
        size *= scale
        size[min_ix] = min_side
    return tuple(size)


def get_ax_size(ax):
    x = ax.get_xlim()
    y = ax.get_ylim()
    x_side = x[1] - x[0]
    y_side = y[1] - y[0]
    return x_side, y_side


def get_render_size(ax):
    f = ax.get_figure()
    return f.get_figwidth(), f.get_figheight()


def set_spines(ax, status=(0, 0, 0, 0)):
    for spine, s in zip(ax.spines.values(), status):
        spine.set_visible(s)


def set_ticks(ax, xticks="none", yticks="none"):
    ax.xaxis.set_ticks_position(xticks)
    ax.yaxis.set_ticks_position(yticks)


def create_cmap(c_array: List[str], name: str = "custom_cmap") -> Colormap:
    return mcolors.ListedColormap(c_array, name=name)


def get_cmap_colors(color: Colors):
    """This utility function allow different color input
    
    1) colormap name
    2) colormap instance
    3) color name, list of color name
    
    """
    cmap = None
    if isinstance(color, str):
        cmap = cm.get_cmap(color)
    elif isinstance(color, Colormap):
        cmap = color
    else:
        return [to_hex(c, keep_alpha=True) for c in color]

    return [to_hex(cmap(i), keep_alpha=True) for i in range(cmap.N)]


def color_mapper_cat(types: Union[List[Any], np.ndarray],
                     c_array: Optional[List[str]] = None,
                     cmap: Colors = None,
                     ) -> Dict:
    """
    
    Args:
        types: All input types
        c_array: The color array that maps to the types
        cmap: An array of colors or colormap


    Returns:
        {type: color}
        
    """
    N = len(types)
    types = np.array(types)
    _, idx = np.unique(types, return_index=True)
    uni_types = types[np.sort(idx)]
    if c_array is not None:
        if len(c_array) < N:
            raise ValueError(f"The length of input color array {len(c_array)} does not match types {N}")
        else:
            cmapper = dict(zip(types, c_array))
            return {k: cmapper[k] for k in uni_types}
    if cmap is not None:
        all_colors = []
        colors_pool = get_cmap_colors(cmap)
        while len(all_colors) < N:
            all_colors += colors_pool

        return dict(zip(uni_types, all_colors))


def color_mapper_val(values: Union[List[Any], np.ndarray],
                     c_array: Optional[List[str]] = None,
                     cmap: Colors = None, ) -> List[str]:
    if not isinstance(values, np.ndarray):
        values = np.ndarray(values)
    vmin = np.nanmin(values)
    vmax = np.nanmax(values)
    norm = mcolors.Normalize(vmin=vmin, vmax=vmax)
    if c_array is not None:
        cmap = create_cmap(c_array)
    mapper = cm.ScalarMappable(norm=norm, cmap=cmap)
    return [to_hex(mapper.to_rgba(v), keep_alpha=True) for v in values]
