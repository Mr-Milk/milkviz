import matplotlib.pyplot as plt
import numpy as np
from upsetplot import UpSet


def upset(
        data,
        names=None,
        orient="v",
        min_subset_size=None,
        max_subset_size=None,
        min_degree=None,
        max_degree=None,
        show_counts=True,
        show_percentages=False,
        figure=None,
        **kwargs,
) -> UpSet:
    """Upset plot for intersections between arbitrary sets

    Unlike `venn`, this will not consider duplicates

    Parameters
    ----------
    data :
        A series of anything, set will be auto computed for it
    names :
        The name for each set
    orient : {'v',  'h'}
    min_subset_size :
        Minimum/Maximum size threshold of a subset to be shown in the plot.
    max_subset_size :
    min_degree :
        Minimum/Maximum degree of a subset to be shown in the plot
    max_degree :
    show_counts :
        Whether to label the intersection size bars
        with the cardinality of the intersection.
    show_percentages :
        Whether to label the intersection size bars
        with the percentage of the intersection relative to the total dataset.
    figure :
        A user input figure instance
    kwargs: Pass to :class:`upsetplot.UpSet`

    """
    try:
        from upsetplot import UpSet
        from upsetplot import from_contents
    except ImportError:
        raise ImportError("Try `pip install UpSetPlot`")

    if figure is None:
        figure = plt.gcf()
    params = dict(
        orientation="vertical" if orient == "h" else "horizontal",
        min_subset_size=min_subset_size,
        max_subset_size=max_subset_size,
        min_degree=min_degree,
        max_degree=max_degree,
        show_counts=show_counts,
        show_percentages=show_percentages,
        **kwargs
    )
    if names is None:
        names = [f"Set{i}" for i in range(len(data))]
    data = [np.unique(d) for d in data]
    contents = dict(zip(names, data))
    data = from_contents(contents)
    p = UpSet(data, **params)
    p.plot(fig=figure)
    return p
