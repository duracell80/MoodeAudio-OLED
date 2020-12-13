#!/bin/bash


ps -ef | grep "python /home/pi/MoodeAudio-OLED/moode-oled-mod.py" | grep -v grep | awk '{print $2}' | xargs kill

python /home/pi/MoodeAudio-OLED/moode-oled-shutdown.py

mpc stop

#sudo shutdown -h now