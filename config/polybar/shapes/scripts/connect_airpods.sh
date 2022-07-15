#!/bin/sh

MAC_ADDR="34:28:40:05:86:D9"

if [ $(bluetoothctl info $MAC_ADDR | grep "Connected: yes" | wc -c) -ne 0 ]
then
  bluetoothctl disconnect $MAC_ADDR
elif [ $(bluetoothctl show | grep "Powered: yes" | wc -c) -ne 0 ]
then
  bluetoothctl connect $MAC_ADDR
fi
