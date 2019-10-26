#!/bin/bash

ps -ef | grep "python /home/pi/MoodeAudio-OLED/moode-oled.py" | grep -v grep | awk '{print $2}' | xargs kill


sudo python /home/pi/MoodeAudio-OLED/moode-oled-splash.py

sudo python /home/pi/MoodeAudio-OLED/moode-oled-mod.py &