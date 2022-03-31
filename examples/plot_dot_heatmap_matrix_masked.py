"""
Triangle Dot heatmap Example
==============================

Here shows how to draw a triangle dot heatmap and dot heatmap + matrix heatmap

"""
import numpy as np
import milkviz as mv
from milkviz import mask_triu

# %%
# First let's create some random data
# -------------------------------------
#
shape = (15, 15)
colors = np.random.randint(1, 100, shape)
sizes = np.random.randint(1, 100, shape)
matrix = np.random.randint(1, 100, shape)
labels = ["Apple", "Avocado", "Banana", "Blueberries", "Coconut",  "Kiwifruit", "Lemon",
          "Mango", "Olives", "Papaya", "Persimmon", "Plum", "Quince", "Soursop", "Watermelon"]


# %%
# Using masked array to create triangle
# ----------------------------------------
# You can replace all unwanted values into `NaN`
#
sizes = mask_triu(sizes)
matrix = mask_triu(matrix)
mv.dot_heatmap(sizes, colors, matrix, xticklabels=labels)

