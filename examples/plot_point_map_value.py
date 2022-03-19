"""
Point map Example (Continuous data)
===================================

Here shows how to draw the point map

"""

import numpy as np
import milkviz as mv

# %%
# First let's create some random data
# -------------------------------------
#
x = np.random.randint(0, 100, 1000)
y = np.random.randint(0, 100, 1000)
values = np.random.randint(0, 100, 1000)


# %%
# Create the cell map
# ----------------------------
#
mv.point_map(x, y, values=values)
