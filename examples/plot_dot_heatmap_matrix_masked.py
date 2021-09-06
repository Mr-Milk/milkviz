"""
Triangle Dot heatmap Example
==============================

Here shows how to draw a triangle dot heatmap and dot heatmap + matrix heatmap

"""
import numpy as np
import milkviz as mv
from milkviz.utils import mask_triu

# %%
# First let's create some random data
# -------------------------------------
#
shape = (10, 10)
colors = np.random.randn(*shape)
sizes = np.random.randn(*shape)
matrix = np.random.randn(*shape)
labels = ["apple", "banana", "Coconut", "Plum", "Kiwifruit",
          "Mango", "Papaya", "Persimmon", "Quince", "Soursop"]


# %%
# Using masked array to create triangle
# ----------------------------------------
# You can replace all unwanted values into `NaN`
#
sizes = mask_triu(sizes)
matrix = mask_triu(matrix)
mv.dot_heatmap(sizes, colors, matrix, xticklabels=labels, sizes=(1, 400))

