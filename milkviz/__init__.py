from matplotlib import cm

from ._bubble import bubble
from ._cell_map import point_map, polygon_map, point_map3d
from ._clustermap import anno_clustermap
# from ._dot import dot
from ._dot_matrix import dot, dot_heatmap
from ._graph import graph
from ._stacked_bar import stacked_bar
from ._upset import upset
from ._venn import venn
from .colormap import echarts, tailwind, retro_metro, river_nights, dutch_field, spring_pastels
from .utils import mask_triu

cm.register_cmap(cmap=echarts)
cm.register_cmap(cmap=tailwind)
cm.register_cmap(cmap=retro_metro)
cm.register_cmap(cmap=dutch_field)
cm.register_cmap(cmap=river_nights)
cm.register_cmap(cmap=spring_pastels)
