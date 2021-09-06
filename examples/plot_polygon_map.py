"""
Polygon map Example
=====================================

Polygon map is similar to point map, but it can't draw links

"""

import numpy as np
import milkviz as mv


# %%
# First let's create some random data
# -------------------------------------
#

def generate_polygon():
    upper = np.random.randint(0, 100)
    lower = np.random.randint(0, 100)
    size = np.random.randint(4, 10)
    if lower > upper:
        lower, upper = upper, lower
    if lower == upper:
        upper += 2
    x = np.random.randint(lower, upper, (size))
    y = np.random.randint(lower, upper, (size))
    return [(i, j) for i, j in zip(x, y)] + [(x[0], y[0])]


polygons = [generate_polygon() for _ in range(100)]
types = np.random.choice(list("abcdefghijklmnopqrstux"), 100)
values = np.random.randint(0, 100, (100))

# %%
# Create the polygon map with categorical data
# ---------------------------------------------
#
mv.polygon_map(polygons, types=types)

# %%
# Create the polygon map with continuous data
# ----------------------------------------------
#
mv.polygon_map(polygons, values=values)
