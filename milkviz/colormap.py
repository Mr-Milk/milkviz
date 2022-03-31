"""Custom colormap in milkviz"""

from matplotlib.colors import ListedColormap

ECHARTS16 = [
    "#5470c6", "#91cc75", "#fac858", "#ee6666", "#9a60b4", "#73c0de", "#3ba272", "#fc8452",
    "#27727b", "#ea7ccc", "#d7504b", "#e87c25", "#b5c334", "#fe8463", "#26c0c0", "#f4e001"
]
TAILWIND20 = [
    "#1d4ed8", "#60a5fa", "#c2410c", "#fb923c", "#15803d", "#86efac", "#b91c1c", "#f87171", "#7e22ce", "#c084fc",
    "#a16207", "#facc15", "#be185d", "#f472b6", "#374151", "#9ca3af", "#4d7c0f", "#a3e635", "#0369a1", "#38bdf8"
]
RETRO_METRO = ["#ea5545", "#f46a9b", "#ef9b20", "#edbf33", "#ede15b", "#bdcf32", "#87bc45", "#27aeef", "#b33dc6"]
DUTCH_FIELD = ["#e60049", "#0bb4ff", "#50e991", "#e6d800", "#9b19f5", "#ffa300", "#dc0ab4", "#b3d4ff", "#00bfa0"]
RIVER_NIGHTS = ["#b30000", "#7c1158", "#4421af", "#1a53ff", "#0d88e6", "#00b7c7", "#5ad45a", "#8be04e", "#ebdc78"]
SPRING_PASTELS = ["#fd7f6f", "#7eb0d5", "#b2e061", "#bd7ebe", "#ffb55a", "#ffee65", "#beb9db", "#fdcce5", "#8bd3c7"]

echarts = ListedColormap(ECHARTS16, name="echarts", N=16)
tailwind = ListedColormap(TAILWIND20, name="tailwind", N=20)

retro_metro = ListedColormap(RETRO_METRO, name="retro_metro", N=9)
dutch_field = ListedColormap(DUTCH_FIELD, name="dutch_field", N=9)
river_nights = ListedColormap(RIVER_NIGHTS, name="river_nights", N=9)
spring_pastels = ListedColormap(SPRING_PASTELS, name="spring_pastels", N=9)
