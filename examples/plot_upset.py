"""
Upset plot Example
==========================

Here shows how to draw upset plot

"""
import numpy as np
import pandas as pd

import milkviz as mv

# %%
# Data input for upset plot
# -------------------------------------

# A list of any sequence, intersections between lists will be computed for you, duplicates will not considred
# 
# Noted that this is the difference from input in venn diagram.
#
mammals = ['Cat', 'Dog', 'Horse', 'Sheep', 'Pig', 'Cattle', 'Rhinoceros', 'Moose']
herbivores = ['Horse', 'Sheep', 'Cattle', 'Moose', 'Rhinoceros']
domesticated = ['Dog', 'Chicken', 'Horse', 'Sheep', 'Pig', 'Cattle', 'Duck']


# %%
# Create the upset plot
# ----------------------------
#
mv.upset([mammals, herbivores, domesticated], names=['mammals', 'herbivores', 'domesticated'])

