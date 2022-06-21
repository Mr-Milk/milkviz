from typing import NewType, Union, Optional, List, Tuple

import numpy as np
from matplotlib.colors import Colormap

OneDimAny = Union[str, List, np.ndarray, None]
OneDimNum = Union[List[int], List[float], np.ndarray, None]

Colors = Union[str, Colormap, None]
Text = Optional[str]
Pos = Union[Tuple[float, float], Tuple[float, float, float, float], None]
Size = Union[Tuple[float, float], None]
