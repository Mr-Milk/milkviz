"""
Annotated heatmap Example
==========================

Here shows how to draw annotated heatmap

"""
import numpy as np
import milkviz as mv

# %%
# First let's create some random data
# -------------------------------------
#
import seaborn as sns
p = sns.load_dataset("penguins").dropna()
df = p.set_index(["species", "island", "sex"])
df.columns.name = "col"
df


# %%
# Create the heatmap
# ----------------------------
#
mv.anno_clustermap(df, row_colors=["species", "island", "sex"], col_label="col", z_score=0)
