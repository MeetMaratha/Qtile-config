# --==[ Widget Base ]==--

from libqtile import widget
from extras import RectDecoration

# This font mustn't be modified.
icon_font = 'SauceCodePro Nerd Font'
#icon_font = 'Roboto Medium'

defaults = dict(
  font = 'SauceCodePro Nerd Font',
  fontsize = 10,
  padding = None,
)

def base(bg: str, fg: str) -> dict:
  return {
    'background': bg,
    'foreground': fg,
  }

def decoration(side: str = 'both') -> dict:
  radius = {'left': [8, 0, 0, 8], 'right': [0, 8, 8, 0]}
  return { 'decorations': [
    RectDecoration(
      filled = True,
      radius = radius.get(side, 8),
      use_widget_background = True,
    )
  ]}

def font(fontsize: int) -> dict:
  return {
    'font': icon_font,
    'fontsize': fontsize,
  }

def icon(bg: str, fg: str) -> dict:
  return {
    **base(bg, fg),
    **font(15),
  }

def spacer(bg: str) -> object:
  return widget.Spacer(background = bg)