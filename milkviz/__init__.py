from ._bubble import bubble
from ._cell_map import point_map, polygon_map
from ._clustermap import anno_clustermap
from ._dot_matrix import dot_heatmap
from ._graph import graph
from ._stacked_bar import stacked_bar
# from ._upset import upset
from ._venn import venn
from .colormap import echarts, tailwind, retro_metro, river_nights, dutch_field, spring_pastels

from .utils import register_colormap

register_colormap("echarts", cmap=echarts)
register_colormap("tailwind", cmap=tailwind)
register_colormap("retro_metro", cmap=retro_metro)
register_colormap("dutch_field", cmap=dutch_field)
register_colormap("river_nights", cmap=river_nights)
register_colormap("spring_pastels", cmap=spring_pastels)
