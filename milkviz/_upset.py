from typing import Optional, List, Any

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

from milkviz.utils import doc


@doc
def upset(
        data: List[List[Any]],
        names: Optional[List[str]] = None,
        orient: str = "v",
        min_subset_size: Optional[int] = None,
        max_subset_size: Optional[int] = None,
        min_degree: Optional[int] = None,
        max_degree: Optional[int] = None,
        show_counts: bool = True,
        show_percentages: bool = False,
        fig: Optional[Figure] = None,
        **kwargs,
) -> Figure:
    """Upset plot for intersections between arbitary sets

    This is simply a wrapper around `upsetplot <https://github.com/jnothman/UpSetPlot>`_

    Unlike `venn`, this will not consider duplicates

    Args:
        data: A series of anything, set will be auto computed for it
        names: The name for each set
        orient: "v" or "h"
        {min, max}_subset_size: Minimum/Maximum size threshold of a subset to be shown in the plot.
        {min, max}_degree: Minimum/Maximum degree of a subset to be shown in the plot
        show_counts: Whether to label the intersection size bars with the cardinality of the intersection.
        show_percentages: Whether to label the intersection size bars with the percentage of the intersection relative to the total dataset.

        **kwargs: Pass to `upsetplot.UpSet <https://upsetplot.readthedocs.io/en/stable/api.html#upsetplot.UpSet>`_

    Returns:
        A `matplotlib.figure.Figure` object

    """
    try:
        from upsetplot import UpSet
        from upsetplot import from_contents
    except ImportError:
        raise ImportError("Extra dependencies needed, Try `pip install UpSetPlot`")

    if fig is None:
        fig = plt.gcf()
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
    p = UpSet(data, **params).plot(fig=fig)
    # No a good thing to do here to prevent jupyter to show the plot twice

    return fig
