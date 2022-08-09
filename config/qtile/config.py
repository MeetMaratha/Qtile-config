
from libqtile import bar, layout, widget, qtile
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
import os
import subprocess
from libqtile.widget.generic_poll_text import GenPollText
from libqtile.widget.battery import BatteryState
from libqtile.log_utils import logger

from libqtile import hook

# Colors

colors = {
    "bg" : "#1f1d2e",
    "fg" : "#e0def4",
    "fg_gutter" : "#ff0000",
    "active" : "#c77dff",
    "focused" : "#ade8f4",
    "other_screen_focused" : "#0077b6",
    "inactive" : "#6c757d",
    'low_bg' : "#212529",
    'low_fg' : "#e5383b",
    "border_focus" : "#c77dff",
    "border_normal" : "#6c757d"
}

# Custome Widgets

# Backlight
class MyBacklight:
    def __init__(self) -> None:
        self.path_bright = os.path.join('/', 'sys', 'class', 'backlight', 'amdgpu_bl0', 'brightness')
        self.path_max = os.path.join('/', 'sys', 'class', 'backlight', 'amdgpu_bl0', 'max_brightness')
        self.icons = [
            "", # Low
            "", # < 50
            "", # < 75
            "" # Full
        ]

    def _update(self):
        with open(self.path_bright, "r") as f:
            self.curr = int(f.read().split("\n")[0])
        with open(self.path_max, "r") as f:
            self.max = int(f.read().split("\n")[0])

    def draw(self):
        self._update()
        percent = self.curr / self.max
        if percent <= 0.25 : char = self.icons[0]
        elif percent <= 0.50 : char = self.icons[1]
        elif percent <= 0.75 : char = self.icons[2]
        else : char = self.icons[3]
        char += f" {int(percent*100)}%"
        result = subprocess.check_output(["echo", char])
        return result.decode("utf-8").replace('\n', '')

# Battery
class MyBattery:
    def __init__(self) -> None:
        self.path_now = os.path.join('/', 'sys', 'class', 'power_supply', 'BAT0', 'energy_now')
        self.path_max = os.path.join('/', 'sys', 'class', 'power_supply', 'BAT0', 'energy_full')
        self.path_status = os.path.join('/', 'sys', 'class', 'power_supply', 'BAT0', 'status')
        self.icons_discharging = [
            "", # <10
            "", # < 20
            "", # < 30
            "", # <40
            "", # <50
            "", # <60
            "", # <70
            "", # <80
	    "", # <90
            "" # Full
        ]

        self.icons_charging = [
	    "", # If charging
            "" # Full
        ]

    def _update(self):
        with open(self.path_now, "r") as f:
            self.curr = int(f.read().split("\n")[0])
        with open(self.path_max, "r") as f:
            self.max = int(f.read().split("\n")[0])
        with open(self.path_status, "r") as f:
            self.status = f.read().split("\n")[0]
        self.percentage = self.curr / self.max
        
    def _chageIcon(self):
        if self.status == 'Charging' or self.status == 'Unknown' : self._charging()
        else : self._discharging() 

    def _discharging(self):
        if self.percentage <= 0.1 : self.char = self.icons_discharging[0]        
        elif self.percentage <= 0.2 : self.char = self.icons_discharging[1]        
        elif self.percentage <= 0.3 : self.char = self.icons_discharging[2]        
        elif self.percentage <= 0.4 : self.char = self.icons_discharging[3]        
        elif self.percentage <= 0.5 : self.char = self.icons_discharging[4]        
        elif self.percentage <= 0.6 : self.char = self.icons_discharging[5]        
        elif self.percentage <= 0.7 : self.char = self.icons_discharging[6]        
        elif self.percentage <= 0.8 : self.char = self.icons_discharging[7]        
        elif self.percentage <= 0.9 : self.char = self.icons_discharging[8]        
        else : self.char = self.icons_discharging[9]     

    def _charging(self):
        if self.percentage < 1.0 : self.char = self.icons_charging[0]
        else : self.char = self.icons_charging[1]

    def draw(self):
        self._update()
        self._chageIcon()
        self.char += f"{int(self.percentage*100)}%"
        result = subprocess.check_output(["echo", self.char])
        return result.decode("utf-8").replace('\n', '')

class MyVolume:
    def __init__(self):
        self.icons = [
            "\ufc5d", # Mute
            "\uf028" # Not mute
        ]
        self.icon = None
        self.cmd = 'pamixer --get-volume-human'
    
    def _getVolume(self):
        temp = subprocess.Popen([self.cmd], stdout=subprocess.PIPE, shell=True)
        out, _ = temp.communicate()
        self.volume = out.decode("utf-8").replace('\n', '')
    
    def _getIcon(self):
        if self.volume == "muted" : self.icon = self.icons[0]
        else : self.icon = self.icons[1]
    
    def draw(self):
        self._getVolume()
        self._getIcon()
        self.char = self.icon + f" {self.volume}" if self.volume != "muted" else self.icon
        result = subprocess.check_output(["echo", self.char]) 
        return result.decode("utf-8").replace('\n', '')

# Initalizing those widgets function
backlight = MyBacklight()
#battery = MyBattery()
volume = MyVolume()

# Some constant values
mod = "mod4"
terminal = guess_terminal()
home = os.path.expanduser('~')
launcher_location = "/home/meet/.config/qtile/scripts/launcher.sh"


keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    # Key([mod], "r", lazy.spawn(), desc="Spawn a command using a prompt widget"),

    # Custom
    # Volume
    Key([], "XF86AudioMute", lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -2%")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +2%")),

    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +10%")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 10%-")),

    # Screenshot
    Key([], "Print", lazy.spawn("xfce4-screenshooter -r")),
    Key([], "Print", lazy.spawn("flameshot gui")),

    # Rofi Menu
    Key([mod], "r", lazy.spawn(f"bash {launcher_location}"), desc="Rofi Menu"),
    # Key([], "XF86TouckpadOn", lazy.spawn("pcmanfm"))

]

workspaces = [
    {"name": " ", "key": "1", "matches": [Match(wm_class = 'Alacritty')]},
    {"name": "", "key": "2", "matches": [Match(wm_class = 'firefox')]},
    {"name": "", "key": "3", "matches": [Match(wm_class = 'pcmanfm')]},
    {"name": "", "key": "4", "matches": [Match(wm_class = 'Steam')]},
    {"name": "", "key": "5", "matches": [Match(wm_class = 'vlc'), Match(wm_class = 'Audacious')]},
    {"name": " ", "key": "6", "matches": [Match(wm_class = 'code')]},
    {"name": " ", "key": "7", "matches": []},
]

groups = []
for workspace in workspaces:
    matches = workspace["matches"] if "matches" in workspace else None
    groups.append(Group(workspace["name"], matches=matches, layout="monadtall"))
    keys.append(Key([mod], workspace["key"], lazy.group[workspace["name"]].toscreen()))
    keys.append(Key([mod, "shift"], workspace["key"], lazy.window.togroup(workspace["name"])))

layouts = [
    layout.Columns(
        border_focus = colors["border_focus"], 
        border_width=3,
        border_normal = colors["border_normal"],
        margin = 3),        
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


screens = [
    Screen(
        top=bar.Bar(
            [
                widget.Spacer(
                    length = 3,
                    background = colors["bg"]),
                widget.Image(
                    background = colors["bg"],
                    filename = "~/.icons/kora-light-panel/apps/scalable/archlinux.svg",
                    margin_y = 3,
                    mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(f"bash {launcher_location}")}
                ),
                widget.Spacer(
                    length = 5,
                    background = colors["bg"]),
                # widget.CurrentLayout(),
                widget.GroupBox(
                    background = colors["bg"],
                    active = colors["active"],
                    inactive = colors["inactive"],
                    padding_x = 5,
                    margin_y = 3,
                    font = 'FontAwesome',
                    fontsize = 16,
                    highlight_method = 'text',
                    spacing = -5,
                ),
                widget.Sep(
                    linewidth = 350,
                    padding = 5,
                    foreground = colors["bg"],
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
                widget.Systray(
                    background = colors["bg"],
                ),
                widget.GenPollText(
                    func = volume.draw,
                    update_interval = 0.2,
                    background = colors["bg"],
                    foreground = colors["fg"],
                    font = 'RobotoMono',
                    fontsize = 14,
		    mouse_callbacks = {
			'Button1' : lambda : qtile.cmd_spawn("pavucontrol")	
		    }
                ),
                widget.GenPollText(
                    func = backlight.draw,
                    update_interval = 0.2,
                    background = colors["bg"],
                    foreground = colors["fg"],
                    font = 'RobotoMono',
                    fontsize = 14
                ),
 #               widget.GenPollText(
 #                   func = battery.draw,
 #                   update_interval = 2,
 #                   background = colors["bg"],
 #                   foreground = colors["fg"],
 #                   font = 'RobotoMono',
 #                   fontsize = 14
 #               ),
                widget.Clock(
                    format = "%H:%M %p",
                    background = colors["bg"],
                    font = "Roboto Condensed",
                    foreground = colors["fg"]),
                widget.Image(
                    background = colors["bg"],
                    filename = "/home/meet/.icons/Tela-blue/24/panel/system-devices-information.svg",
                    mouse_callbacks = {
                        'Button1': lambda: qtile.cmd_spawn("bash /home/meet/.config/qtile/scripts/powermenu.sh")
                    }
                ),
                widget.CurrentLayoutIcon(
                    background = colors["bg"],
                    font = 'Roboto Medium',
                    foreground = colors["fg"],
                    mouse_callbacks = {
                        'Button1' : lazy.next_layout() # Switch to next next layout on left click
                    },
                    scale = 0.65
                )
            ],
            24,
            opacity = 0.7,
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client. Add floating windows here.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
        
        # Custom
        Match(wm_class = "Blueberry"), # Bluetooth
        Match(wm_class = "Nitrogen"), # Wallpaper manager
#        Match(wm_class = "Steam"), # Steam
        Match(wm_class = "task manager"), # Task Manager
        Match(wm_class = "Nm-connection-editor"), # Network editor
        Match(wm_class = "Pavucontrol"), # Volume Manager
        Match(wm_class = "Audacious"), # Music Player
        Match(wm_class = "Transmission-gtk"), # Torrent downloader
        Match(wm_class = "Lxappearance") # Theme customizer
        # Match(wm_class = "TelegramDesktop") # Telegram Messenger
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True


# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/autostart.sh')
    subprocess.call([home])
