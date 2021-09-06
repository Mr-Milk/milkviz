"""
Dot heatmap Example
======================

Here shows how to draw dot heatmap

"""
import numpy as np
import milkviz as mv

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
# Create the dot heatmap
# ----------------------------
#
mv.dot_heatmap(sizes, colors, xticklabels=labels)

