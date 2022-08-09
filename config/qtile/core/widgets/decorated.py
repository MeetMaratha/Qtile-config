# Inspired by Axyl's polybar.
# https://github.com/axyl-os

from libqtile import qtile
from libqtile.bar import CALCULATED, STRETCH
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
import os
import subprocess
from libqtile import widget as widdgets

from core.widgets.base import base, decoration, font, icon
from extras import CheckUpdates, GroupBox, modify, TextBox, widget
from utils import color

terminal = guess_terminal()
tags: list[str] = [
  '', '', '', '', '', '', '', 
  # '', '', '', '', '切', '',
]
launcher_location = '/home/meet/.config/rofi/launcher.sh'


# Custom

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
        self.icon = ''
      else:
        self.icon = ''
    else:
      self.icon = ''

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

battery = MyBattery()
bluetooth = MyBluetooth()

# Custom end

bar: dict = {
  'background': color[16],
  'border_color': color[16],
  'border_width': 4,
  'margin': [10, 10, 0, 10],
  'opacity': 1,
  'size': 18,
}

def sep(fg: str, offset = 0, padding = 8) -> TextBox:
  return TextBox(
    **icon(None, fg),
    offset = offset,
    padding = padding,
    text = '',
  )

def powerline(bg: str, color: str) -> TextBox:
  return TextBox(
    **base(bg, color),
    **font(31),
    offset = -1,
    padding = -4,
    text = '',
    y = -1,
  )

def logo(bg: str, fg: str) -> TextBox:
  return modify(
    TextBox,
    **decoration(),
    **icon(bg, fg),
    mouse_callbacks = { 'Button1': lazy.restart() },
    # mouse_callbacks = { 'Button1': lambda: qtile.cmd_spawn(f"bash {launcher_location}") },
    offset = 4,
    padding = 17,
    text = '',
  )

def groups(bg: str) -> GroupBox:
  return GroupBox(
    **font(15),
    background = bg,
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
      update_interval = 0.1,
      mouse_callbacks = {
	      'Button1' : lambda : qtile.cmd_spawn("pavucontrol")
	      }
    ),
  ]

def updates(bg: str, fg: str) -> list:
  return [
    TextBox(
      **icon(bg, fg),
      offset = -2,
      text = '',
      x = -6,
      mouse_callbacks = {
	      'Button1' : lambda: qtile.cmd_spawn(f"{terminal} -e sudo pacman -Syu")
	      }
    ),
    modify(
      CheckUpdates,
      **base(bg, fg),
      **decoration('right'),
      colour_have_updates = fg,
      colour_no_updates = fg,
      display_format = '{updates} updates  ',
      distro = 'Arch_checkupdates',
      initial_text = 'Loading...  ',
      no_update_string = 'No updates  ',
      padding = 0,
      update_interval = 3600,
      mouse_callbacks = {
	      'Button1' : lambda: qtile.cmd_spawn(f"{terminal} -e sudo pacman -Syu")
	      }
    ),
  ]

def window_name(bg: str, fg: str) -> object:
  return widget.WindowName(
    **base(bg, fg),
    format = '{name}',
    max_chars = 60,
    width = CALCULATED,
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
	    'Button1' : lambda : qtile.cmd_spawn('nm-connection-editor')
    }
  )]

def blue(bg: str, fg: str) -> list:
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
      func = bluetooth.update,
      update_interval = 0.2,
      fontsize = 14,
      mouse_callbacks = {
        'Button1' : lazy.spawn('blueberry'),
        'Button2' : bluetooth._changePower,
        'Button3' : bluetooth._connect
      }
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
      update_interval = 0.2,
    ),
  ]

# def tray(bg: str, fg: str) -> list:
#   return [
    
#   ]

def clock(bg: str, fg: str) -> list:
  return [
    modify(
      TextBox,
      **decoration('left'),
      **icon(bg, fg),
      offset = 2,
      text = '',
      x = 4,
    ),

    widget.Clock(
      **base(bg, fg),
      **decoration('right'),
      format = '%A - %I:%M %p ',
      padding = 6,
    ),
  ]

widgets: list = [
  widget.Spacer(length = 4),
  logo(color[4], color[16]),
  sep(color[8], offset = -8),
  groups(None),
  sep(color[8], offset = 4, padding = 4),
  *volume(color[5], color[16]),
#  powerline(color[5], color[1]),
#  *updates(color[1], color[16]),

  widget.Spacer(),
  window_name(None, color[17]),
  widget.Spacer(),

  *wifi(color[2], color[16]),
  powerline(color[2], color[3]),
  *blue(color[3], color[16]),
  powerline(color[3], color[6]),
  *batt(color[6], color[16]),
  # *tray(color[6], color[16]),
  sep(color[8]),
  *clock(color[5], color[16]),
  widget.Spacer(length = 4),
]


