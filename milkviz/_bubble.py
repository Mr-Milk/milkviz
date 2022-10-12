import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

from legendkit import SizeLegend, Colorbar
from milkviz.utils import set_default


def bubble(data=None,
           x=None,
           y=None,
           hue=None,
           size=None,
           cmap=None,
           norm=None,
           vmin=None,
           vmax=None,
           sizes=(10, 250),
           size_norm=None,
           dtype=None,
           legend_kw=None,
           cbar_kw=None,
           ax=None,
           **kwargs,
           ) -> mpl.axes.Axes:
    """Bubble plot

    Parameters
    ----------
    data :
    x :
    y :
    hue :
    size :
    cmap : default to "RdBu"
    norm :
    vmin :
    vmax :
    sizes :
    size_norm :
    dtype:
    legend_kw : dict
        The options to configure legend
    cbar_kw : dict
        The options to configure colorbar
    ax :

    """
    ax = set_default(ax, plt.gca())
    legend_kw = set_default(legend_kw, {})
    cbar_kw = set_default(cbar_kw, {})

    if data is not None:
        x = data[x].to_numpy()
        y = data[y].to_numpy()
        hue = data[hue].to_numpy() if hue is not None else None
        size = data[size].to_numpy() if size is not None else None

    if size is None:
        raise ValueError("At least `size` must be provided")

    if size_norm is None:
        size_norm = Normalize()
        size_norm.autoscale(size)
    circ_size = size_norm(size) * (sizes[1] - sizes[0]) + sizes[0]
    bubbles = ax.scatter(x, y,
                         s=circ_size,
                         c=hue,
                         cmap=cmap,
                         norm=norm,
                         vmin=vmin,
                         vmax=vmax,
                         **kwargs,
                         )

    legend_options = dict(
        loc="out right upper",
        dtype=dtype
    )
    legend_options = {**legend_options, **legend_kw}
    SizeLegend(sizes=circ_size, array=size, ax=ax, **legend_options)
    if hue is not None:
        cbar_options = dict(
            loc="out right lower",
        )
        cbar_options = {**cbar_options, **cbar_kw}
        Colorbar(bubbles, ax=ax, **cbar_options)

    return ax
