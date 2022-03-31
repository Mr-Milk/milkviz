"""
Dot plot Example
======================

Here shows how to draw dot plot

"""
import numpy as np
import milkviz as mv

# %%
# First let's create some random data
# -------------------------------------
#
shape = (10, 3)
colors = np.repeat([['#3A3226', '#CB1B45', '#F75C2F']], 10, axis=0)
sizes = np.random.randint(1, 100, shape)
matrix = np.random.randint(1, 100, shape)
labels = ["apple", "banana", "Coconut", "Plum", "Kiwifruit",
          "Mango", "Papaya", "Persimmon", "Quince", "Soursop"]

# %%
# Create the dot heatmap
# ----------------------------
#
mv.dot(sizes, colors, yticklabels=labels)

