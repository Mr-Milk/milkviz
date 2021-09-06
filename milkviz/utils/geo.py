import math

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
