from typing import NewType, Union, Optional, List, Tuple

import numpy as np
from matplotlib.colors import Colormap

OneDimAny = NewType("OneDim", Union[str, List, np.ndarray, None])
OneDimNum = NewType("OneDim", Union[List[int], List[float], np.ndarray, None])

Colors = NewType("Colors", Union[str, Colormap, None])
Text = NewType("Text", Optional[str])
Pos = NewType("Pos", Union[Tuple[float, float], Tuple[float, float, float, float], None])
Size = NewType("Size", Union[Tuple[float, float], None])
