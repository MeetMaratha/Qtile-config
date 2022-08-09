# --==[ Screens ]==--

from libqtile import bar
from libqtile.config import Screen
import os
import numpy as np

import core.widgets as widgets

BAR = bar.Bar(**widgets.bar)
DIR = os.path.expanduser('~/Pictures/Wallpaper/')

image_names = next(os.walk(DIR))[2]
image_name = np.random.choice(image_names)

config = {
  'wallpaper': f'~/Pictures/Wallpaper/{image_name}',
  'wallpaper_mode': 'fill',
}

screens = [
  Screen(**config, top = BAR), # type: ignore
]
