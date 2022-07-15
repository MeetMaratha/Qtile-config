from libqtile import widget, bar
from libqtile.config import Screen
from colors import colors
from widget.battery import my_Battery


widget_defaults = dict(
    font = "FontAwesome",
    fontsize = 12,
    padding = 3,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                # widget.CurrentLayout(),
                widget.GroupBox(
                    background = colors["groupBox"]["bg"],
                    active = colors["groupBox"]["active"],
                    borderwidth = 0,
                    foreground = colors["groupBox"]["fg"],
                    inactive = colors["groupBox"]["fg_gutter"],
                    margin_x = 5,
                    font = "FontAwesome",
                    highlight_method = 'text',
                    rounded = True,
                    highlight_color = colors["groupBox"]["other_screen_focused"]
                ),
                widget.Prompt(),
                widget.Spacer(
                    background = colors["bg"]
                ),
                widget.WindowName(
                    background = colors["bg"],
                    font = 'Roboto Medium',
                    empty_group_string = ' ',
                    foreground = colors["fg"],
                    format = '{name}',
                    max_chars = 50
                ),
                widget.Spacer(
                    background = colors["bg"]
                ),
                widget.Systray(
                    background = colors["bg"]
                ),
                widget.Volume(
                    background = colors["bg"],
                    emoji = False,
                    font = 'FontAwesome',
                    fontsize = 10,
                    fmt = "{}",
                    theme_path = '/home/meet/.icons/kora-light-panel/panel/24/',
                    update_interval = 1,
                    mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn("pavucontrol")}
                ),
                myBattery(),
                widget.Clock(
                    format = "%d/%m/%y %H:%M %p",
                    background = colors["bg"],
                    font = "Roboto Medium",
                    foreground = colors["fg"]),
                widget.QuickExit(),
                widget.CurrentLayoutIcon(
                    background = colors["bg"],
                    font = 'Roboto Medium',
                    foreground = colors["fg"]
                )
            ],
            24,
            opacity = 0.7
        ),
    ),
]