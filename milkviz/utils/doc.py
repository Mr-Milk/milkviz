import re
from inspect import getdoc

PARAMETERS_DOCSTRINGS = dict(
    ax="Pre-existing axes for the plot. Or a new one will be created.",
    data="Data use to plot, should be a dataframe",
    x="Either a key in data or a numpy array",
    y="Either a key in data or a numpy array",
    hue="The color array that map to marker colors",
    size="The size array that map to marker sizes",
    cmap="The colormap to be used, either a cmap name or a `matplotlib.cm.ColorMap`",
    xticklabels="Text to put on the x-axis ticks",
    yticklabels="Text to put on the y-axis ticks",
    xlabel="Title for x-axis",
    ylabel="Title for y-axis",
    types="The types array that tells the types",
    values="The values array that tells the values",
    vminmax="Remap your values to another range",
    sizes="The size range of circle markers, (min, max)",
    no_spines="If True, will turn off the frame of the plot",
    no_ticks="If True, will turn off both major and minor ticks",
    legend="If True, show legend",
    legend_title="The title of legend",
    legend_pos="A 2-tuple (x, y) to set the position of legend, the origin is at the upper left",
    legend_ncol="Number of columns the legend will have",
    dtype="Only coerce the value display on the legend, does not affect plotting",

    return_obj="A `matplotlib.axes.Axes` instance",
    cbar_title="The title of colorbar",
    cbar_pos="A 2-tuple (x, y) or 4-tuple (x, y, frac of fig width, frac of fig height) "
             "to place colorbar, the origin is the same as plot",
    cbar_size="A tuple (width, height) in inches",
    cbar_ticklabels="Set the ticklabels of colorbar"
)


def doc(obj):
    docstring = getdoc(obj)
    for param_name, content in PARAMETERS_DOCSTRINGS.items():
        pattern = re.compile(f"""(\[{param_name}\])""")
        docstring = re.sub(pattern, content, docstring)
    obj.__doc__ = docstring
    return obj
