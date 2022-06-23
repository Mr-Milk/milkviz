"""
Point map 3D Example (Categorical data)
========================================

Here shows how to draw the point map in 3D

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
z = np.random.randint(0, 100, 1000)
types = np.random.choice(list("abcdef"), 1000)

# %%
# Create the point map
# ----------------------------
#
mv.point_map3d(x, y, z, types=types, legend_kw={"title": "Type"})

