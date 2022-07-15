from libqtile import layout
from colors import colors

layouts = [
    layout.Columns(
        border_focus = colors["layout"]["border_focus"], 
        border_width=4,
        border_normal = colors["layout"]["border_normal"]),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]