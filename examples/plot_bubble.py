"""
Bubble plot Example
======================

Here shows how to draw dot plot

"""
import numpy as np
import milkviz as mv

# %%
# First let's create some random data
# -------------------------------------
#
x = np.arange(10, 20)
y = np.log2(x) * 5
size = np.random.randint(3, 10, 10)
color = np.random.randint(3, 10, 10)


# %%
# Create the dot heatmap
# ----------------------------
#
mv.bubble(x=x, y=y, size=size, hue=color, sizes=(100, 400))

