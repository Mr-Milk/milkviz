import math
from typing import Optional

import numpy as np


# modified from https://stackoverflow.com/questions/34372480/
def rotate_points(px, py, origin, angle):
    """
    Rotate points counterclockwise by a given angle around a given origin.

    The angle should be given in degrees.
    """
    angle = math.radians(angle)
    ox, oy = origin

    qx = ox + np.cos(angle) * (px - ox) - np.sin(angle) * (py - oy)
    qy = oy + np.sin(angle) * (px - ox) + np.cos(angle) * (py - oy)
    return qx, qy


def normalize(arr: np.ndarray,
              vmin: Optional[float] = None,
              vmax:  Optional[float] = None,
              ):
    if (vmin is None) & (vmax is None):
        return arr

    amin = np.amin(arr)
    amax = np.amax(arr)
    narr = (arr - amin) / (amax - amin)
    vmin = 0 if vmin is None else vmin
    vmax = 1 if vmax is None else vmax
    return narr * (vmax - vmin) + vmin

