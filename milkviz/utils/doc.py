import re
from inspect import getdoc

PARAMETERS_DOCSTRINGS = dict(
    ax="Pre-existing axes for the plot. Or a new one will be created.",
    data="Data use to plot, should be a dataframe",
    x="Either a key in data or a numpy array",
    y="Either a key in data or a numpy array",
    hue="The color array that map to marker colors",
    size="The size array that map to marker sizes",
    color="The colormap for the markers",
    xticklabels="Text to put on the x-axis ticks",
    yticklabels="Text to put on the y-axis ticks",
    xlabel="Title for x-axis",
    ylabel="Title for y-axis",
    types="The types array that tells the types",
    values="The values array that tells the values",
    sizes="The size range of circle markers, (min, max)",
    no_spines="If True, will turn off the frame of the plot",
    no_ticks="If True, will turn off both major and minor ticks",
    size_legend_title="Title for size legend",
    cbar_title="Title for colorbar",
    return_obj="A `matplotlib.axes.Axes` instance",
)


def doc(obj):
    docstring = getdoc(obj)
    for param_name, content in PARAMETERS_DOCSTRINGS.items():
        pattern = re.compile(f"""(\[{param_name}\])""")
        docstring = re.sub(pattern, content, docstring)
    obj.__doc__ = docstring
    return obj
