#!/bin/sh
nitrogen --set-zoom-fill --random ~/Pictures/Wallpaper/ &
picom --experimental-backends &
#nm-applet &
#blueberry-tray &
libinput-gestures-setup start &
#cbatticon &
playerctld daemon &
dunst &
