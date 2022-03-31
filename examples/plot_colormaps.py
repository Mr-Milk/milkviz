"""
Custom colormap in milkviz
===========================

Currently, I made 6 categorical colormap

- echarts (16): Taken from Echarts.js v5.0
- tailwind (20): Taken from TailwindCSS v3.0
- retro_metro (9)
- dutch_field (9)
- river_nights (9)
- spring_pastels (9)

"""
import milkviz.colormap as mc
import seaborn as sns

# %%
# echarts
# -------------------------------------
# You can either call it by name or import it
#
sns.color_palette("echarts", n_colors=16)
sns.color_palette(mc.echarts.colors)


# %%
# tailwind
# ----------------------------
# This is a mocking of tab20
#
sns.color_palette("tailwind", n_colors=20)


# %%
# Retro Metro
# ----------------------------
#
sns.color_palette("retro_metro", n_colors=9)


# %%
# Dutch Field
# ----------------------------
#
sns.color_palette("dutch_field", n_colors=9)


# %%
# River Nights
# ----------------------------
#
sns.color_palette("river_nights", n_colors=9)


# %%
# Spring Pastels
# ----------------------------
#
sns.color_palette("spring_pastels", n_colors=9)

