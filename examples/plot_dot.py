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
shape = (3, 10)
colors = np.repeat(['#3A3226', '#CB1B45', '#F75C2F'], 10).reshape(10, 3).T
sizes = np.random.randn(*shape)
matrix = np.random.randn(*shape)
labels = ["apple", "banana", "Coconut", "Plum", "Kiwifruit",
          "Mango", "Papaya", "Persimmon", "Quince", "Soursop"]

# %%
# Create the dot heatmap
# ----------------------------
#
mv.dot(sizes, colors, yticklabels=labels)

