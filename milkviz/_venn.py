from collections import Counter

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from typing import Set


def find_intersection(*arr_list):
    count = 0
    counter = [Counter(arr) for arr in arr_list]
    max_ix = np.argmax([len(c) for c in counter])
    max_size_counter = counter[max_ix]
    counter.pop(max_ix)
    for k1 in max_size_counter.keys():
        count += min(max_size_counter[k1], *[c.get(k1, 0) for c in counter])
    return count


def venn(
        data,
        names=None,
        colors=None,
        alpha=None,
        subset_labels=None,
        normalize_to=1.0,
        weighted=True,
        ax=None,
) -> Axes:
    """Venn diagram for 2 & 3 Sets

    This is a wrapper around
    `matplotlib-venn <https://github.com/konstantint/matplotlib-venn>`_,
    allows you to input raw data and compute intersection for you.

    Parameters
    ----------
    data :
        1) A list of sets
        2) A list of list, will compute intersection, duplication
        will be considered.
        3) A list of number denotes the regions in venn diagram
        in the following order: (10, 01, 11)
        or (100, 010, 110, 001, 101, 011, 111)
    names :
        The name for each set
    colors :
        The color for each set
    alpha :
        The alpha value for each set
    subset_labels :
        The label for each small regions, usually denotes the size,
        following the order as described before
    normalize_to :
        specifies the total (on-axes) area of the circles to be drawn.
        Sometimes tuning it (together with the overall figure size)
        may be useful to fit the text labels better.
    weighted :
        If True, the circle area is weighted by the size of sets
    ax :

    """
    try:
        from matplotlib_venn import venn2, venn3, \
            venn2_unweighted, venn3_unweighted
    except ImportError:
        raise ImportError("Try `pip install matplotlib-venn`")
    if ax is None:
        ax = plt.gca()
    s = len(data)
    colors = ("#F1C266", "#65BBC4", "#F3A292") if colors is None else colors
    # compute intersection for user
    if not isinstance(data[0], (Set, int)):
        if s == 2:
            s1, s2 = data
            s1s2 = find_intersection(s1, s2)
            s1, s2 = len(s1), len(s2)
            data = (s1 - s1s2, s2 - s1s2, s1s2)
            venn_num = 2
        else:
            s1, s2, s3 = data
            s1s2 = find_intersection(s1, s2)
            s1s3 = find_intersection(s1, s3)
            s2s3 = find_intersection(s2, s3)
            s1s2s3 = find_intersection(s1, s2, s3)
            s1, s2, s3 = len(s1), len(s2), len(s3)
            data = (s1 - s1s2 - s1s3 + s1s2s3,
                    s2 - s1s2 - s2s3 + s1s2s3,
                    s1s2 - s1s2s3,
                    s3 - s1s3 - s2s3 + s1s2s3,
                    s1s3 - s1s2s3,
                    s2s3 - s1s2s3,
                    s1s2s3)
            venn_num = 3
    # user input is regions area
    elif isinstance(data[0], int):
        if s == 3:
            venn_num = 2
        elif s == 7:
            venn_num = 3
        else:
            raise ValueError(f"You have {s} input. Does not match ordering of"
                             f"(10, 01, 11) or "
                             f"(100, 010, 110, 001, 101, 011, 111)")
    # user input is sets
    else:
        if s > 3:
            raise ValueError(f"You have {s} sets. Venn diagram is usually for "
                             f"showing intersection between "
                             f"no more than 3 sets,"
                             f"please use upset plot instead for sets > 3.")
        venn_num = s

    if venn_num == 2:
        venn_func = venn2 if weighted else venn2_unweighted
        patch_order = ('10', '01', '11')
    elif venn_num == 3:
        venn_func = venn3 if weighted else venn3_unweighted
        patch_order = ('100', '010', '110', '001', '101', '011', '111')
    else:
        raise ValueError(f"Intersection only happens "
                         f"between more than 2 sets.")

    v = venn_func(data, names, colors, normalize_to=normalize_to, ax=ax)
    alpha_array = [0.4 for _ in range(len(patch_order))]
    if alpha is not None:
        if isinstance(alpha, (int, float)):
            alpha_array = [alpha for _ in range(len(patch_order))]
        else:
            if len(alpha) >= s:
                alpha_array = alpha

    for patch_id, a in zip(patch_order, alpha_array):
        p = v.get_patch_by_id(patch_id)
        if p is not None:
            p.set_alpha(a)

    if subset_labels is not None:
        for patch_id, label in zip(patch_order, subset_labels):
            lb = v.get_label_by_id(patch_id)
            if lb is not None:
                lb.set_text(label)

    return ax
