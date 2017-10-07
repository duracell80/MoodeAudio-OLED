#!/usr/bin/python
# Author: Suwat Saisema
# Date: 5-Oct-2017

import time

# Adafruit Library
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

# MPD Clint
from mpd import MPDClient, MPDError, CommandError

# Raspberry Pi pin configuration:
RST = 24
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# 128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

# MPD Client
class MPDFetch(object):
    def __init__(self, host='localhost', port=6600):
        self._mpd_client = MPDClient()
        self._mpd_client.timeout = 10

        self._host = host
        self._port = port

    def connect(self):
        self._mpd_client.connect(self._host, self._port)

        #while True:
        #    self._mpd_client.status()
        #    time.sleep(1)

    def disconnect(self):
        self._mpd_client.close()
        self._mpd_client.disconnect()

    def _play_pause(self):
        self._mpd_client.pause()
        #return False

    def _next_track(self):
        self._mpd_client.next()
        #return False

    def _prev_track(self):
        self._mpd_client.previous()
        #return False

    def info(self):
        song_info = self._mpd_client.currentsong()

        # Artist Name
        if 'artist' in song_info:
            artist = song_info['artist']
        else:
            artist = 'Unknown Artist'
        # Song Name
        if 'title' in song_info:
            title = song_info['title']
        else:
            title = 'Unknown Title'

    def stat():
        song_stats = self._mpd_client.status()

        # Song time
        elapsed = song_stats['elapsed']
        duration = song_stats['duration']
        countdown = float(duration) - float(elapsed)
        m,s = divmod(float(countdown), 60)
        h,m = divmod(m, 60)
        time = "%d:%02d:%02d" % (h, m, s)

        # Volume
        vol = song_stats['volume']

        # Audio
        if 'audio' in song_stats:
            bit = song_stats['audio'].split(':')[1]
            frequency = song_stats['audio'].split(':')[0]
            bitrate = song_stat['bitrate']

            audio_info =  bit + "bit " + frequency + "kHz" + bitrate + "kbps"
        else:
            audio_info = ""

class FetchError(Exception):
    """Fatal fetch data error."""

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
    font_artist = ImageFont.truetype('arialuni.ttf', 14)
    font_title = ImageFont.truetype('arialuni.ttf', 12)
    font_info = ImageFont.truetype('arialuni.ttf', 10)

    # Create drawing object.
    draw = ImageDraw.Draw(image)

    # MPD Connect
    client = MPDFetch()
    client.connect()

    # Draw data to display
    while True:
        # Clear image buffer by drawing a black filled box.
        draw.rectangle((0,0,width,height), outline=0, fill=0)

        # Fetch data
        info = client.info()
        artist = info['artist']
        title = info['title']

        stat = client.stat()
        time = stat['time']
        vol = stat['vol']
        audio = stat['audio_info']

        # Draw text.
        draw.text((0, ), unicode(artist).center(24,' '), font=font_artist, fill=255)
        draw.text((0,15), unicode(title).center(24, ' '), font=font_title, fill=255)
        draw.text((0,30), time, font=font_info, fill=255)
        draw.text((86,30),"Vol " +  str(vol) , font=font_info, fill=255)
        draw.text((0,45), audio, font=font_info, fill=255)

        # Draw the image buffer.
        disp.image(image)
        disp.display()

        # Pause briefly before drawing next frame.
        time.sleep(1)

if __name__ == "__main__":
    import sys
    try:
        main()

    # Catch fatal fetch data errors
    except FetchError as e:
        sys.stderr.write("Fatal fetch data error: %s" % e)
        sys.exit(1)

    # Catch all other non-exit errors
    except Exception as e:
        sys.stderr.write("Unexpected exception: %s" % e)
        sys.exit(1)

    # Catch the remaining exit errors
    except:
        sys.exit(0)