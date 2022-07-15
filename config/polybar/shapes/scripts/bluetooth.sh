#!/bin/sh

if [ $(bluetoothctl show | grep "Powered: yes" | wc -c) -eq 0 ]
then
  echo "%{F#985918}"      # If the bluetooth controller is powered off
elif [ $(bluetoothctl info | grep "Connected: yes" | wc -c) -ne 0 ]
  then 
    echo "%{F#0079F5}"    # If it is connected to a device
else
  echo "%{F#F50100}"      # If controller is powered on but not connected to a device
fi

