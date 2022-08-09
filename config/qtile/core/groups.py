# --==[ Groups ]==--

from libqtile.config import Group, Key, Match
from libqtile.lazy import lazy

from core.keys import keys, mod
import core.widgets as widgets

# Icons & Tags
groups, tag = [ ], widgets.tag

# Workspaces
for g in (
  ('1', tag[0], '', [Match(wm_class = 'Alacritty')]),
  ('2', tag[1], 'max', [Match(wm_class = 'firefox')]),
  ('3', tag[2], '', [Match(wm_class = 'pcmanfm')]),
  ('4', tag[3], '', [Match(wm_class = 'code')]),
  ('5', tag[4], 'max', [Match(wm_class = 'steam'), Match(wm_class = 'lutris')]),
  ('6', tag[5], 'max', [Match(wm_class = 'vlc'), Match(wm_class = 'Audacious')]),
  ('7', tag[6], '', [ ]),
):
  args = {'label': g[1], 'layout': g[2], 'matches': g[3]}
  groups.append(Group(name = g[0], **args)) # type: ignore

# Key Bindings
for i in groups:
  keys.extend([
    # mod1 + letter of group = switch to group
    Key([mod], i.name, lazy.group[i.name].toscreen(toggle = True)),

    # mod1 + shift + letter of group = move focused window to group
    Key([mod, 'shift'], i.name, lazy.window.togroup(i.name)),
  ])
