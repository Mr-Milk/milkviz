"""
Point map Example (Categorical data)
=====================================

Here shows how to draw the point map

"""

import numpy as np
import milkviz as mv

# %%
# First let's create some random data
# -------------------------------------
#
np.random.seed(0)
x = np.random.randint(0, 100, 1000)
y = np.random.randint(0, 100, 1000)
types = np.random.choice(list("abcdefghijklmnopqrstux"), 1000)

# %%
# Create the point map
# ----------------------------
#
mv.point_map(x, y, types=types,
             legend_kw={"title": "Type", "title_align": "center", "ncol": 2})

# %%
# It's possible to add some links
# ---------------------------------
#
links = [np.random.choice([i for i in range(1000)], 2) for _ in range(50)]
mv.point_map(x, y, types, links=links,
             legend_kw={"title": "Type", "title_align": "center", "ncol": 2})

