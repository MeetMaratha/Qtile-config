# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile import bar, layout, hook, drawer, qtile
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
import os, subprocess, math
from qtile_extras import widget  # type: ignore
from qtile_extras.widget import modify  # type: ignore
from qtile_extras.widget.decorations import (         # type: ignore
  BorderDecoration, RectDecoration
)
from libqtile.widget import base as basewidget
from libqtile.widget import groupbox

# from extras import GroupBox, widget

mod, alt = "mod4", "mod1"
terminal = guess_terminal()

# Colors
color = [
  "#45475A",
  "#F38BA8",
  "#A6E3A1",
  "#F9E2AF",
  "#89B4FA",
  "#F5C2E7",
  "#94E2D5",
  "#BAC2DE",

  "#585B70",
  "#F38BA8",
  "#A6E3A1",
  "#F9E2AF",
  "#89B4FA",
  "#F5C2E7",
  "#94E2D5",
  "#A6ADC8",

  "#1E1E2E",
  "#CDD6F4"
]

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.window.toggle_floating(), desc="Make Window floating"),
    Key([mod], 'c', lazy.window.center(), desc="Make window center"),
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
    Key([mod], "r", lazy.spawn('/home/meet/.config/rofi/launcher.sh'), desc="Spawn a command using a prompt widget"),

    # Custom
    Key([mod, 'control'], 'b', lazy.hide_show_bar(), desc = "Hide bar"),
    Key([mod, alt], 'r', lazy.restart(), desc = "restart qtile config"),
    Key([mod, alt], 's', lazy.spawn('kill -9 -1'), desc = "basically logout/ Kill X Server"),
    Key([mod], 't', lazy.spawn('pcmanfm'), desc = "Open File Manager"),
    # Backlight
    Key([], 'XF86MonBrightnessDown', lazy.spawn('brightnessctl set 5%-')),
    Key([], 'XF86MonBrightnessUp', lazy.spawn('brightnessctl set +5%')),

    # Volume
    Key([ ], 'XF86AudioMute', lazy.spawn('pamixer --toggle-mute')),
    Key([ ], 'XF86AudioLowerVolume', lazy.spawn('pamixer --decrease 5')),
    Key([ ], 'XF86AudioRaiseVolume', lazy.spawn('pamixer --increase 5')),

    # Player
    Key([ ], 'XF86AudioPlay', lazy.spawn('playerctl play-pause')),
    Key([ ], 'XF86AudioPrev', lazy.spawn('playerctl previous')),
    Key([ ], 'XF86AudioNext', lazy.spawn('playerctl next')),

    # Screenshot
    Key([], "Print", lazy.spawn("flameshot gui")),

    # Power Menu
    Key([mod], 'q', lazy.spawn("/home/meet/.config/rofi/powermenu.sh")),
]

groups = []
tag = ['', '', '', '', '', '', '',]

for g in (
  ('1', tag[0], '', [Match(wm_class = 'Alacritty')]),
  ('2', tag[1], 'max', [Match(wm_class = 'firefox')]),
  ('3', tag[2], '', [Match(wm_class = 'pcmanfm'), Match(wm_class = 'Thunar')]),
  ('4', tag[3], '', [Match(wm_class = 'code')]),
  ('5', tag[4], 'max', [Match(wm_class = 'steam'), Match(wm_class = 'lutris'), Match(wm_class = 'heroic')]),
  ('6', tag[5], 'max', [Match(wm_class = 'vlc'), Match(wm_class = 'Audacious')]),
  ('7', tag[6], '', [ ]),
):
  args = {'label': g[1], 'layout': g[2], 'matches': g[3]}
  groups.append(Group(name = g[0], **args)) # type: ignore

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

config_layouts = {
  'single_border_width': 0,
  'border_width': 0,
  'single_margin': 10,
  'margin': 10,
  'border_normal': color[17],
  'border_focus': color[5],
}

layouts = [
    layout.MonadTall(
        **config_layouts,
        min_ratio = 0.30,
        max_ratio = 0.70,
        change_ratio = 0.02,
    ),
    layout.Max(**config_layouts),
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

widget_defaults = dict(
    font="SauceCodePro Nerd Font",
    fontsize=10,
    padding=3,
)
extension_defaults = widget_defaults.copy()
icon_font = "SauceCodePro Nerd Font"

# Custom Widget configuration stuff

def base(bg: str, fg: str) -> dict:
  return {
    'background': bg,
    'foreground': fg,
  }

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

def decoration(side: str = 'both') -> dict:
  radius = {'left': [8, 0, 0, 8], 'right': [0, 8, 8, 0]}
  return { 'decorations': [
    RectDecoration(
      filled = True,
      radius = radius.get(side, 8),
      use_widget_background = True,
    )
  ]}

def framed(self, border_width, border_color, pad_x, pad_y, highlight_color=None):
  return TextFrame(
    self, border_width, border_color, pad_x, pad_y, highlight_color=highlight_color
  )

class TextFrame(drawer.TextFrame):
  def __init__(self, layout, border_width, border_color, pad_x, pad_y, highlight_color=None):
    super().__init__(layout, border_width, border_color, pad_x, pad_y, highlight_color)

  def draw(self, x, y, rounded=True, fill=False, line=False, highlight=False, invert=False):
    self.drawer.set_source_rgb(self.border_color)
    opts = [
      x,
      y,
      self.layout.width + self.pad_left + self.pad_right,
      self.layout.height + self.pad_top + self.pad_bottom,
      self.border_width,
    ]
    if line:
      if highlight:
        self.drawer.set_source_rgb(self.highlight_color)
        self.drawer.fillrect(*opts)
        self.drawer.set_source_rgb(self.border_color)

      opts[1] = 0 if invert else self.height - self.border_width
      opts[3] = self.border_width

      self.drawer.fillrect(*opts)
    elif fill:
      if rounded:
        self.drawer.rounded_fillrect(*opts)
      else:
        self.drawer.fillrect(*opts)
    else:
      if rounded:
        self.drawer.rounded_rectangle(*opts)
      else:
        self.drawer.rectangle(*opts)
    self.drawer.ctx.stroke()
    self.layout.draw(x + self.pad_left, y + self.pad_top)

  def draw_line(self, x, y, highlighted, inverted):
    self.draw(x, y, line=True, highlight=highlighted, invert=inverted)


class TextBox(basewidget._TextBox):
  '''A flexible textbox that can be updated from bound keys, scripts, and qshell.'''

  def __init__(
    self,
    text = ' ',
    width = bar.CALCULATED,
    offset = 0,
    x = 0,
    y = 0,
    **config,
  ):
    basewidget._TextBox.__init__(self, text = text, width = width, **config)
    self.add_offset = offset
    self.add_x = x
    self.add_y = y

  def cmd_update(self, text):
    '''Update the text in a TextBox widget'''
    self.update(text)

  def cmd_get(self):
    '''Retrieve the text in a TextBox widget'''
    return self.text

  def calculate_length(self):
    if self.text:
      if self.bar.horizontal:
        return min(self.layout.width, self.bar.width) \
          + self.actual_padding * 2 + self.add_offset
      else:
        return min(self.layout.width, self.bar.height) \
          + self.actual_padding * 2 + self.add_offset
    else:
      return 0

  def draw(self):
    if not self.can_draw():
      return
    self.drawer.clear(self.background or self.bar.background)

    # size = self.bar.height if self.bar.horizontal else self.bar.width
    self.drawer.ctx.save()

    if not self.bar.horizontal:
      # Left bar reads bottom to top
      if self.bar.screen.left is self.bar:
        self.drawer.ctx.rotate(-90 * math.pi / 180.0)
        self.drawer.ctx.translate(-self.length, 0)

      # Right bar is top to bottom
      else:
        self.drawer.ctx.translate(self.bar.width, 0)
        self.drawer.ctx.rotate(90 * math.pi / 180.0)

    # If we're scrolling, we clip the context to the scroll width less the padding
    # Move the text layout position (and we only see the clipped portion)
    if self._should_scroll:
      self.drawer.ctx.rectangle(
        self.actual_padding,
        0,
        self._scroll_width - 2 * self.actual_padding,
        self.bar.size,
      )
      self.drawer.ctx.clip()

    size = self.bar.height if self.bar.horizontal else self.bar.width

    self.layout.draw(
      (self.actual_padding or 0) - self._scroll_offset + self.add_x,
      int(size / 2.0 - self.layout.height / 2.0) + 1 + self.add_y,
    )
    self.drawer.ctx.restore()

    self.drawer.draw(
      offsetx=self.offsetx, offsety=self.offsety, width=self.width, height=self.height
    )

    # We only want to scroll if:
    # - User has asked us to scroll and the scroll width is smaller than the layout (should_scroll=True)
    # - We are still scrolling (is_scrolling=True)
    # - We haven't already queued the next scroll (scroll_queued=False)
    if self._should_scroll and self._is_scrolling and not self._scroll_queued:
      self._scroll_queued = True
      if self._scroll_offset == 0:
        interval = self.scroll_delay
      else:
        interval = self.scroll_interval
      self._scroll_timer = self.timeout_add(interval, self.do_scroll)

class _GroupBase(groupbox._GroupBase):
  def __init__(self, **config):
    super().__init__(**config)

  def _configure(self, qtile, bar):
    basewidget._Widget._configure(self, qtile, bar)

    if self.fontsize is None:
      calc = self.bar.height - self.margin_y * 2 - self.borderwidth * 2 - self.padding_y * 2
      self.fontsize = max(calc, 1)

    self.layout = self.drawer.textlayout(
      "", "ffffff", self.font, self.fontsize, self.fontshadow
    )
    self.layout.framed = framed.__get__(self.layout)
    self.setup_hooks()

  def drawbox(
    self,
    offset,
    text,
    bordercolor,
    textcolor,
    highlight_color=None,
    width=None,
    rounded=False,
    block=False,
    line=False,
    highlighted=False,
    inverted=False,
  ):
    self.layout.text = self.fmt.format(text)
    self.layout.font_family = self.font
    self.layout.font_size = self.fontsize
    self.layout.colour = textcolor
    if width is not None:
      self.layout.width = width
    if line:
      pad_y = [
        (self.bar.height - self.layout.height - self.borderwidth) / 2,
        (self.bar.height - self.layout.height + self.borderwidth) / 2,
      ]
      if highlighted:
        inverted = False
    else:
      pad_y = self.padding_y

    if bordercolor is None:
      # border colour is set to None when we don't want to draw a border at all
      # Rather than dealing with alpha blending issues, we just set border width
      # to 0.
      border_width = 0
      framecolor = self.background or self.bar.background
    else:
      border_width = self.borderwidth
      framecolor = bordercolor

    framed = self.layout.framed(border_width, framecolor, 0, pad_y, highlight_color)
    y = self.margin_y
    if self.center_aligned:
      for t in basewidget.MarginMixin.defaults:
        if t[0] == "margin":
          y += (self.bar.height - framed.height) / 2 - t[1]
          break
    if block and bordercolor is not None:
      framed.draw_fill(offset, y, rounded)
    elif line:
      framed.draw_line(offset, y, highlighted, inverted)
    else:
      framed.draw(offset, y, rounded)

class GroupBox(_GroupBase, groupbox.GroupBox):
  defaults = [
    ("invert", False, "Invert line position when 'line' highlight method isn't highlighted."),
    ("rainbow", False, "If set to True, 'colors' will be used instead of '*_screen_border'."),
    (
      "colors",
      False,
      "Receive a list of strings."
      "Allows each tag to be an independent/unique color when selected, this overrides 'active'."
    ),
  ]

  def __init__(self, **config):
    super().__init__(**config)
    self.add_defaults(GroupBox.defaults)

  def draw(self):
    self.drawer.clear(self.background or self.bar.background)

    def color(index: int) -> str:
      try:
        return self.colors[index]
      except IndexError:
        return "FFFFFF"

    offset = self.margin_x
    for i, g in enumerate(self.groups):
      to_highlight = False
      is_block = self.highlight_method == "block"
      is_line = self.highlight_method == "line"

      bw = self.box_width([g])

      if self.group_has_urgent(g) and self.urgent_alert_method == "text":
        text_color = self.urgent_text
      elif g.windows:
        text_color = color(i) if self.colors else self.active
      else:
        text_color = self.inactive

      if g.screen:
        if self.highlight_method == "text":
          border = None
          text_color = self.this_current_screen_border
        else:
          if self.block_highlight_text_color:
            text_color = self.block_highlight_text_color

          if self.bar.screen.group.name == g.name:
            if self.qtile.current_screen == self.bar.screen:
              if self.rainbow and self.colors:
                border = color(i) if g.windows else self.inactive
              else:
                border = self.this_current_screen_border
              to_highlight = True
            else:
              if self.rainbow and self.colors:
                border = color(i) if g.windows else self.inactive
              else:
                border = self.this_screen_border
              to_highlight = True

          else:
            if self.qtile.current_screen == g.screen:
              if self.rainbow and self.colors:
                border = color(i) if g.windows else self.inactive
              else:
                border = self.other_current_screen_border
            else:
              if self.rainbow and self.colors:
                border = color(i) if g.windows else self.inactive
              else:
                border = self.other_screen_border

      elif self.group_has_urgent(g) and self.urgent_alert_method in (
        "border",
        "block",
        "line",
      ):
        border = self.urgent_border
        if self.urgent_alert_method == "block":
          is_block = True
        elif self.urgent_alert_method == "line":
          is_line = True
      else:
        border = None

      self.drawbox(
        offset,
        g.label,
        border,
        text_color,
        highlight_color=self.highlight_color,
        width=bw,
        rounded=self.rounded,
        block=is_block,
        line=is_line,
        highlighted=to_highlight,
        inverted=self.invert,
      )
      offset += bw + self.spacing
    self.drawer.draw(offsetx=self.offset, offsety=self.offsety, width=self.width)

class Command(object):
    """Run a command and capture it's output string, error string and exit status"""

    def __init__(self, command):
        self.command = command 

    def run(self, shell=True):
        import subprocess as sp
        process = sp.Popen(self.command, shell = shell, stdout = sp.PIPE, stderr = sp.PIPE)
        self.pid = process.pid
        self.output, self.error = process.communicate()
        self.failed = process.returncode
        return self

    @property
    def returncode(self):
        return self.failed

class MyBluetooth():
  def __init__(self) -> None:
    self.check_power = 'bluetoothctl show | grep "Powered: yes" | wc -l'
    self.check_connection = 'bluetoothctl info | grep "Connected: yes" | wc -l'
    self.power_command = None
  
  def _check_status(self) -> None:
    self.power = int(Command(self.check_power).run().output)
    if self.power == 1:
      self.connected = int(Command(self.check_connection).run().output)
      if self.connected == 1:
        self.icon = ' '
      else:
        self.icon = ' '
    else:
      self.icon = ' '

  def update(self) -> str:
    self._check_status()
    result = subprocess.check_output(["echo", self.icon])
    return result.decode("utf-8").replace('\n', '')
  
  def _changePower(self) -> None:
    if self.power == 1 : cmd = 'bluetoothctl power off'
    else : cmd = 'bluetoothctl power on'
    subprocess.run(cmd, shell=True)
  
  def _connect(self) -> None:
    if self.power == 1:
      if self.connected == 1 : cmd = 'bluetoothctl disconnect 34:28:40:05:86:D9'
      else : cmd = 'bluetoothctl connect 34:28:40:05:86:D9'
      subprocess.run(cmd, shell = True)

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
	          "", # < 20
            "", # < 30
            "", # < 40
            "", # < 60
            "", # < 80
            "", # < 90
            "" # Full
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
        if self.percentage <= 0.2 : self.char = self.icons_charging[0]
        elif self.percentage <= 0.3 : self.char = self.icons_charging[1]
        elif self.percentage <= 0.4 : self.char = self.icons_charging[2]
        elif self.percentage <= 0.6 : self.char = self.icons_charging[3]
        elif self.percentage <= 0.8 : self.char = self.icons_charging[4]
        elif self.percentage <= 0.9 : self.char = self.icons_charging[5]
        elif self.percentage <= 1.0 : self.char = self.icons_charging[6]

    def draw(self):
        self._update()
        self._chageIcon()
        self.char += f" {int(self.percentage*100)}%  "
        result = subprocess.check_output(["echo", self.char])
        return result.decode("utf-8").replace('\n', '')


battery = MyBattery()
bluetooth = MyBluetooth()

# Custom Widgets

def logo(bg: str, fg: str) -> TextBox:
  return modify(
    TextBox,
    **decoration(),
    **icon(bg, fg),
    # mouse_callbacks = { 'Button1': lazy.restart() },
    mouse_callbacks = { 'Button1': lazy.spawn("/home/meet/.config/rofi/launcher.sh") },
    offset = 4,
    padding = 17,
    text = '',
  )

def sep(fg: str, offset = 0, padding = 8) -> TextBox:
  return TextBox(
    foreground = fg,
    offset = offset,
    padding = padding,
    text = '',
    fontsize = 16,
  )

def volume(bg: str, fg: str) -> list:
  return [
    modify(
      TextBox,
      **decoration('left'),
      **icon(bg, fg),
      text = '',
      x = 4,
    ),
    widget.PulseVolume(
      **base(bg, fg),
      **decoration('right'),
      update_interval = 0.5,
      mouse_callbacks = {
	      'Button1' : lazy.spawn("pavucontrol")
	      },
      font = "Roboto Medium",
      fontsize = 12,
    ),
  ]

def window_name(bg: str, fg: str) -> object:
  return widget.WindowName(
    **base(bg, fg),
    format = '{name}',
    max_chars = 60,
    font = "Roboto Medium",
    fontsize = 12,
    width = bar.CALCULATED,
  )

def wifi(bg: str, fg: str) -> list:
  return [
    widget.WiFiIcon(
    **base(bg, fg),
    **decoration('left'),
    interface = 'wlp1s0',
    padding_y = 4,
    padding_x = 8,
    mouse_callbacks = {
      'Button1' : lazy.spawn("/home/meet/.config/rofi/launcher.sh"),
    }
  )]

def powerline(bg: str, color: str) -> TextBox:
  return TextBox(
    **base(bg, color),
    **font(31),
    offset = -1,
    padding = -4,
    text = '',
    y = -1,
  )

def blue(bg: str, fg: str) -> list:
  return [
    widget.GenPollText(
      **base(bg , fg),
      func = bluetooth.update,
      update_interval = 2,
      fontsize = 14,
      mouse_callbacks = {
        'Button1' : lazy.spawn('blueberry'),
        'Button2' : bluetooth._changePower,
        'Button3' : bluetooth._connect
      },
    ),
  ]

def batt(bg: str, fg: str) -> list:
  return [
    TextBox(
      **icon(bg, fg),
      offset = -2,
      # text = '',
      text = '',
      x = -6,
    ),
    widget.GenPollText(
      **base(bg , fg),
      **decoration('right'),
      func = battery.draw,
      update_interval = 10,
    ),
  ]

def clock(bg: str, fg: str) -> list:
  return [
    modify(
      TextBox,
      **decoration('left'),
      **icon(bg, fg),
      offset = -2,
      text = ' ',
      x = 4,
    ),

    widget.Clock(
      **base(bg, fg),
      **decoration('right'),
      format = '%A - %I:%M %p ',
      padding = 6,
      font = "Roboto Medium",
      fontsize = 12,
    ),
  ]


# Screen


screens = [
    Screen(
        top=bar.Bar(
            [
                # widget.Spacer(),
                logo(color[4], color[16]),
                sep(color[8], offset = -8),
                GroupBox(
                  **font(15),
                  background = None,
                  borderwidth = 1,
                  colors = [
                    color[6], color[5], color[3],
                    color[1], color[4], color[2],
                  ],
                  highlight_color = color[16],
                  highlight_method = 'line',
                  inactive = color[8],
                  invert = True,
                  padding = 7,
                  rainbow = True,
                ),
                sep(color[8], offset = 4, padding = 4),
                *volume(color[5], color[16]),
                widget.Spacer(),
                window_name(None, color[17]),
                widget.Spacer(),
                *wifi(color[2], color[16]),
                powerline(color[2], color[3]),
                *blue(color[3], color[16]),
                powerline(color[3], color[6]),
                *batt(color[6], color[16]),
                sep(color[8]),
                *clock(color[5], color[16]),
                # widget.Spacer(),
            ],
            size = 18,
            margin = [6, 6, -6, 6],
            background = color[16],
            border_width = 4,
            border_color = color[16],
            opacity = 0.8,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
    # Click([], "Button3", lazy.spawn("jgmenu_run")),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False

floating_layout = layout.Floating(
    fullscreen_border_width = 0,
    border_width = 0,
    border_normal = color[17],
    border_focus = color[7],

    float_rules = [
        *layout.Floating.default_float_rules,
        Match(wm_class = [
            'confirmreset',
            'gnome-screenshot',
            'lxappearance',
            'makebranch',
            'maketag',
            'ssh-askpass',
            'blueberry.py',
            'pavucontrol',
            'nm-connection-editor',
            'Xephyr',
            'xfce4-about',
        ]), # type: ignore

        Match(title = [
            'branchdialog',
            'File Operation Progress',
            'minecraft-launcher',
            'Open File',
            'pinentry',
        ]), # type: ignore
    ],
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

# Startup
@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/autostart.sh')
    subprocess.call([home])
