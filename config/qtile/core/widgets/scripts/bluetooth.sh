#!/bin/bash

if [ $(bluetoothctl show | grep "Powered: yes" | wc -l ) -ne 0 ]
then
	if [ $(bluetoothctl info | grep "Connected: yes"| wc -l) -ne 0 ]
	then
		echo "FF0000" # Connected to device
	else
		echo "FFFFFF" # Not connected to device
	fi
else
	echo "00FF00" # Not powered
fi
