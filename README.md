# MoodeAudio-OLED
OLED 128x64 for MoodeAudio

This is a forked version of the original script by naisema with some major tweaks that make the OLED screen output more useful for Internet Radio usage in a hardware project. I gutted the inside of a broken iView ATSC Box in testing. To get the best out of this script cue up your favourite radio stations in a saved playlist so that Moode can feel like a radio device.<br /><br />

![Playing State](https://raw.githubusercontent.com/duracell80/MoodeAudio-OLED/master/example-playing-state.jpg)

<strong>Tweaks</strong><br>
1. Updated install instructions for Moode 6
2. Better handling of metadata from radio stations<br>
3. When "changing stations" the screen will say "Tuning ..."<br>
4. Splashscreen on loading that shows the Moode logo!<br>
5. Display of hostname and IP Address when MPD state shows no media playing<br>
6. Shutdown screen with countdown that can be tied to a GPIO pin

![New Splashscreen](https://raw.githubusercontent.com/duracell80/MoodeAudio-OLED/master/example-splash.jpg)

<br><br><br>

# Installation

1. Login to MoodeAudio with user pi and password moodeaudio
2. Ran raspi-config and enabled i2c and auto login<br><br>

<strong>How To Make Moode Auto Login</strong><br>
Run: sudo raspi-config
Choose Boot Options
Choose Desktop / CLI
Choose Console Autologin
Select Finish, and reboot the pi.

3. Prerequites <br />
   $ sudo apt-get update <br />
   $ sudo apt-get install build-essential python-pip python-dev python-smbus git python-imaging python-mpd<br />
4. Adafruit Python GPIO Library <br />
   $ git clone https://github.com/adafruit/Adafruit_Python_GPIO.git <br />
   $ cd Adafruit_Python_GPIO <br />
   $ sudo python setup.py install <br />
5. Adafruit Python SSD1306 <br />
   $ git clone https://github.com/adafruit/Adafruit_Python_SSD1306.git <br />
   $ cd Adafruit_Python_SSD1306 <br />
   $ sudo python setup.py install <br />
6. Download python script from github <br />
   $ git clone https://github.com/naisema/MoodeAudio-OLED.git <br />
7. Go to MoodAudio UI menu -> Configure -> System -> Local Services
   Enable the metadata file (currentsong.txt) and toggle the LCD Update Engine on <br />
8. Add startup script to /etc/profile.d<br /><br />
   $ sudo cp /home/pi/MoodeAudio-OLED/moode-oled-startup.sh /etc/profile.d/<br /><br />

   The script upon startup will display the splashscreen<br />
   $ python /home/pi/MoodeAudio-OLED/moode-oled-splash.py <br /><br />

   Which will linger for 15 seconds or more before running the main oled-mod script<br />
   $ python /home/pi/MoodeAudio-OLED/moode-oled-mod.py &

9. Optional: Use moode-oled-shutdown.sh script on a GPIO pin (9) in Moode to shutdown the OLED and then the system on button press. Do this by going in the Moode Web UI to Configure -> System -> GPIO Button Handler -> Edit. OR use the script in your favouirte place to safely shutdown the pi. The shutdown -h now command is commented out for your convenience but the screen should show a countdown timer and bring down the volume in a fade out fashion.
<br><br><br>

# Notes
NOTE: The original script remains in this repo, the new one has -mod at the end of the filename. If the original script this was forked from is still running, the modifed script can seek the PID of that script and kill it. Having the main screen script run multiple times causes the "weird characters" on the display. The shutdown script also tries to kill the process of the main script for this reason. If these screen glitches are occuring it's because there are multiple scripts trying to update the same screen once a second. Search your favorite search engine for process kill commands.<br><br>

A helpful command to rescue the screen is<br>
$ sudo pkill -f "python /home/pi/MoodeAudio-OLED/moode-oled-mod.py" & python moode-oled-clear.py <br><br>

If you're editing the bash files in Windows there may be some line end issues, fix these with sed<br>
$ sed -i -e 's/\r$//' ./*.sh
