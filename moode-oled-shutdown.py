#!/usr/bin/python
# Author: Suwat Saisema
# Date: 5-Oct-2017


import sys
import time
import socket
import re 
import os
from socket import error as socket_error

# Delay First Run So That MPD Has Chance To Start
# time.sleep(30)

# Adafruit Library
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw



# System UTF-8
reload(sys)
sys.setdefaultencoding('utf-8')

# Raspberry Pi pin configuration:
RST = 24
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# 128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)


def main():
    # Initialize Library
    disp.begin()

    # Get display width and height.
    width = disp.width
    height = disp.height

    # Clear display
    disp.clear()
    disp.display()

    # Create image buffer.
    # Make sure to create image with mode '1' for 1-bit color.
    image = Image.new('1', (width, height))

    # Load default font.
    font_artist = ImageFont.truetype('/home/pi/MoodeAudio-OLED/Arial-Unicode-Bold.ttf', 14)
    font_title = ImageFont.truetype('/home/pi/MoodeAudio-OLED/Arial-Unicode-Regular.ttf', 13)
    font_info = ImageFont.truetype('/home/pi/MoodeAudio-OLED/Verdana-Italic.ttf', 10)
    font_time = ImageFont.truetype('/home/pi/MoodeAudio-OLED/Verdana.ttf', 13)

    # Create drawing object.
    draw = ImageDraw.Draw(image)

    # First define some constants to allow easy resizing of shapes.
    padding = 2
    shape_width = 20
    top = padding
    bottom = height-padding
    artoffset = 2
    titoffset = 2
    animate = 15
    
    countdown = 31
    

    # Draw data to display
    while True:
        # Clear image buffer by drawing a black filled box.
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        
        countdown = countdown - 1
        if countdown == -1:
            disp.clear()
            disp.display()
            break
        
        # Draw text
        draw.text((20,top), "Moode Audio", font=font_artist, fill=255)
        draw.text((35,20), "Shutdown", font=font_time, fill=255)
        
        #draw.text((padding,45), "Stopped", font=font_time, fill=255)
        draw.text((75,45), "sec: " + str(countdown), font=font_time, fill=255)
        

        # Draw the image buffer.
        disp.image(image)
        disp.display()
        
        # Fade Volume In Steps
        volCmd = 'mpc volume ' + str(countdown*2)
        os.system(volCmd)
        
        
        # Pause briefly before drawing next frame.
        time.sleep(1)
        

if __name__ == "__main__":
    main()