"""
Graph plot Example
===================

Here shows how to draw a graph

"""

import numpy as np
import milkviz as mv

# %%
# First let's create some random data
# -------------------------------------
#
nodes = ["Apple", "Banana", "Grape", "Pineapple", "Orange"]

edges = [("Apple", "Banana"), ("Banana", "Grape"),
         ("Grape", "Pineapple"), ("Banana", "Pineapple"),
         ("Banana", "Orange"), ("Grape", "Orange")]

nodes_size = np.random.randint(0, 100, 5).tolist()
edges_width = np.random.randint(0, 100, 6).tolist()
nodes_color = np.random.randint(0, 100, 5).tolist()
edges_color = np.random.randint(0, 100, 6).tolist()


# %%
# Create the graph
# ----------------------------
#
mv.graph(edges, nodes_size=nodes_size, edges_width=edges_width, nodes_color=nodes_color, edges_color=edges_color)
