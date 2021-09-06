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
x = np.random.randint(0, 100, (100))
y = np.random.randint(0, 100, (100))
types = np.random.choice(list("abcdefghijklmnopqrstux"), 100)

# %%
# Create the point map
# ----------------------------
#
mv.point_map(x, y, types=types)

# %%
# It's possible to add some links
# ---------------------------------
#
links = [np.random.choice([i for i in range(100)], 2) for _ in range(50)]
mv.point_map(x, y, types, links=links)

