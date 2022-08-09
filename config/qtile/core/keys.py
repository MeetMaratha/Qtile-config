# --==[ Key Bindings ]==--

from libqtile.config import Key
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
import os

from extras import bring_to_front

keys, mod, alt = [ ], 'mod4', 'mod1'
terminal = guess_terminal()
launcher_location = os.path.expanduser('~/.config/rofi/launcher.sh')
power_menu_location = os.path.expanduser('~/.config/rofi/powermenu.sh')

for key in [
  # Switch/move between windows
  ([mod], 'h', lazy.layout.left()),
  ([mod], 'l', lazy.layout.right()),
  ([mod], 'j', lazy.layout.down()),
  ([mod], 'k', lazy.layout.up()),

  ([mod, 'shift'], 'h', lazy.layout.shuffle_left()),
  ([mod, 'shift'], 'l', lazy.layout.shuffle_right()),
  ([mod, 'shift'], 'j', lazy.layout.shuffle_down()),
  ([mod, 'shift'], 'k', lazy.layout.shuffle_up()),

  # Increase/decrease window size
#  Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
#  Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
#  Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
#  Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),

  # Window management
  ([mod, 'shift'], 'space', lazy.layout.flip()),
  ([mod], 'm', lazy.layout.maximize()),
  ([mod], 'n', lazy.layout.normalize()),
  ([mod], 'q', lazy.window.kill()),
  ([ ], 'F11', lazy.window.toggle_fullscreen()),

  # Floating window management
  ([mod], 'space', lazy.window.toggle_floating()),
  ([mod], 'c', lazy.window.center()),
  ([mod], 'f', lazy.function(bring_to_front)),

  # Toggle between layouts
  ([mod], 'Tab', lazy.next_layout()),

  # Qtile management
  ([mod, 'control'], 'b', lazy.hide_show_bar()),
  ([mod, 'control'], 's', lazy.shutdown()),
  ([mod, 'control'], 'r', lazy.reload_config()),
  ([mod, alt], 'r', lazy.restart()),

  # Kill X server
  ([mod, alt], 's', lazy.spawn('kill -9 -1')),

  # ----------- # ----------- # ----------- # ----------- #

  # Terminal
  ([mod], 'Return', lazy.spawn(terminal)),

  # Browser
  ([mod], 'b', lazy.spawn('firefox')),

  # File Manager
  ([mod], 't', lazy.spawn('pcmanfm')),

  # Apps Menu
#  ([mod, 'shift'], 'r', lazy.spawn('rofi -show')),
  ([mod], 'r', lazy.spawn(f"bash {launcher_location}")),
#  ([mod], 'd', lazy.spawn('dmenu_run')),

  # Backlight
  ([], 'XF86MonBrightnessDown', lazy.spawn('brightnessctl set 5%-')),
  ([], 'XF86MonBrightnessUp', lazy.spawn('brightnessctl set +5%')),

  # Volume
  ([ ], 'XF86AudioMute', lazy.spawn('pamixer --toggle-mute')),
  ([ ], 'XF86AudioLowerVolume', lazy.spawn('pamixer --decrease 5')),
  ([ ], 'XF86AudioRaiseVolume', lazy.spawn('pamixer --increase 5')),

  # Player
  ([ ], 'XF86AudioPlay', lazy.spawn('playerctl play-pause')),
  ([ ], 'XF86AudioPrev', lazy.spawn('playerctl previous')),
  ([ ], 'XF86AudioNext', lazy.spawn('playerctl next')),

  # Screenshot
  ([], "Print", lazy.spawn("flameshot gui")),

  # Power Menu
  ([mod], 'w', lazy.spawn(f"bash {power_menu_location}")),
]: keys.append(Key(*key)) # type: ignore
