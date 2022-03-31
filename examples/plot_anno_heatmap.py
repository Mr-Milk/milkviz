"""
Annotated heatmap Example
==========================

Here shows how to draw annotated heatmap

"""
import numpy as np
import pandas as pd

import milkviz as mv

# %%
# First let's create some random data
# -------------------------------------
#
import seaborn as sns
p = sns.load_dataset("penguins").dropna()
df = p.set_index(["species", "island", "sex"])
data = np.random.randn(*df.to_numpy().shape)
df = pd.DataFrame(data=data, columns=df.columns, index=df.index)
df.columns.name = "col"
df


# %%
# Create the heatmap
# ----------------------------
#
mv.anno_clustermap(df, row_colors=["species", "island", "sex"],
                   row_legend_padding=0.18,
                   col_label="col", z_score=0)
