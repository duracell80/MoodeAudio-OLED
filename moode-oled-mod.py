#!/usr/bin/python
# Author: Lee Jordan
# Date: 25-Oct-2019


import sys
import time
import socket
import re 
import os
from socket import error as socket_error

# Delay First Run So That MPD Has Chance To Start
time.sleep(15)

# Adafruit Library
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

# MPD Clint
from mpd import MPDClient, MPDError, CommandError, ConnectionError

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


# Update Host Details for Stop State Screen
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("1.1.1.1", 80))

hostname   = socket.gethostname()
hostip     = s.getsockname()[0]

# MPD Client
class MPDConnect(object):
    def __init__(self, host='localhost', port=6600):
        self._mpd_client = MPDClient()
        self._mpd_client.timeout = 10
        self._mpd_connected = False

        self._host = host
        self._port = port

    def connect(self):
        if not self._mpd_connected:
            try:
                self._mpd_client.ping()
            except(socket_error, ConnectionError):
                try:
                    self._mpd_client.connect(self._host, self._port)
                    self._mpd_connected = True
                except(socket_error, ConnectionError, CommandError):
                    self._mpd_connected = False

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

    def fetch(self):        
        
        
        
        
        
        # MPD current song
        song_info = self._mpd_client.currentsong()
        
        
        # MPD Status
        song_stats = self._mpd_client.status()
        
        # State
        state        = song_stats['state']
        
            
        # Volume
        vol = song_stats['volume']
        
        
        # Set some asignments to prevent logic crashes
        bitrate_display = ""
        tunetime = float(0.0)
        
        # Song time
        if 'elapsed' in song_stats:
            elapsed = song_stats['elapsed']
            m,s = divmod(float(elapsed), 60)
            h,m = divmod(m, 60)
            eltime = "%d:%02d:%02d" % (h, m, s)
            
            # Set Up Something Cool Here
            tunetime = float(song_stats['elapsed'])
            
        else:
            eltime ="0:00:00"

        # Audio
        if 'audio' in song_stats:
            bit = song_stats['audio'].split(':')[1]
            frequency = song_stats['audio'].split(':')[0]
            z, f = divmod( int(frequency), 1000 )
            if ( f == 0 ):
                frequency = str(z)
            else:
                frequency = str( float(frequency) / 1000 )
            bitrate = song_stats['bitrate']
            bitrate_display = song_stats['bitrate'] + "kbps"
            
            audio_info =  bit + "bit " + frequency + "kHz " + bitrate + "kbps"
            
            
            
            
            
            
        else:
            audio_info = ""
        
        
        
        
        
        # MOODE current song for Radio Station - Enrich OLED Output
        with open('/var/local/www/currentsong.txt') as nowplaying:
            nowplayingmeta  = list(nowplaying)
            if len(nowplayingmeta) > 0:
                callsign  = nowplayingmeta[1]
            else:
                callsign  = "iNet Radio" 
        
        if 'Radio station' in callsign:
            
            station_long = nowplayingmeta[2][6:None]
            
            if ':' in station_long:
                # Split On Semi Colon
                station_split   = station_long.split(":")
                station_name    = " ".join(station_split[0].split()[:2])
            elif 'Audiophile' in station_long:
                # Replace With AP
                station_name   = station_long.replace("Audiophile", "AP - ")
            elif 'France Musique' in station_long:
                # Replace With AP
                station_name   = station_long.replace("France Musique", "FM - ")
            elif 'Soma FM' in station_long:
                # Split On Dash
                station_split   = station_long.split("-")
                station_name    = " ".join(station_split[1].split()[:2])
            elif 'NME' in station_long:
                # Split On Dash
                station_split   = station_long.split("-")
                station_name    = " ".join(station_split[0].split()[:2])
            elif 'SUB.FM' in station_long:
                # Split On Dash
                station_split   = station_long.split("-")
                station_name    = " ".join(station_split[0].split()[:1])
            else:
                # Keep Only First Three Words
                station_name    = " ".join(station_long.split()[:3])
            
            
            
            
            
            

            # Re-assign Artist as Station Name and Remove Brackets eg (320) or [SomaFM]
            artist = re.sub("[\(\[].*?[\)\]]", "", station_name)
            
            
            # Display Host Name if Station Name Unknown
            if 'Unknown' in artist:
                artist = hostname
            
            # Get Base Bitrate
            if 'audio' in song_stats:
                bitrate_display = "Bitrate: " + song_stats['bitrate'] + "kbps"
            
            
            # Deal with Displaying Bitrate in Place of Now Playing Track Or Display Of Now Playing Track If Present
            if 'title' in song_info:
                
       
                # Now Playing Track Unknown
                if song_info['title'] == 'Unknown':
                    title           = bitrate_display
                else:
                    # Now Playing Track Duplicates Station Name
                    if song_info['title'] == station_name:
                        title           = bitrate_display
                    else:
                        title           = song_info['title']
                        title_length    = len(title)
                        
                        # Now Playing Check For Lack Of Detail Else OK 
                        if title_length < 10:
                            title = bitrate_display
                        
                 
             
                
                
            # Radio Station   
            else:
                # Display Bitrate When Now Playing Track Is Missing (eg Moode Shows 'Streaming source')
                # Prevent Zero Bitrate From Displaying
                if 'audio' in song_stats:
                    bitrate_encoded = nowplayingmeta[8].split("=")
                    if song_stats['bitrate'] == "0":
                        bitrate_display = "Bitrate: VBR"

                    if "VBR" in bitrate_encoded:
                        bitrate_display = "Bitrate: " + song_stats['bitrate'] + "kbps"
                
                title = bitrate_display
                
        
        
            
            # Still Radio Let's Kick It Up A Level with Tuning Message
            if tunetime < 1.5:
                title           = "Tuning ..."
                artist          = ""


        else:
            # Not Radio Station
            # Artist Name
            if 'artist' in song_info:
                artist = song_info['artist']
            else:
                artist = hostname
            # Song Name
            if 'title' in song_info:
                # Song Name - Remove Pipe Expansions
                title_split   = song_info['title'].split("|")
                nowplaying    = title_split[0]
                
                # Now Playing Check For Lack Of Detail Else OK 
                if len(nowplaying) < 3:
                    title = "Bitrate: " + bitrate_display
                else:
                    title = nowplaying
            else:
                title = hostip

        

        audio_info = ""
        return({'state':state, 'artist':artist, 'title':title, 'eltime':eltime, 'volume':int(vol), 'audio_info':audio_info, 'hostname':hostname, 'hostip':hostip})

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

    # MPD Connect
    client = MPDConnect()
    client.connect()

    # Draw data to display
    while True:
        # Clear image buffer by drawing a black filled box.
        draw.rectangle((0,0,width,height), outline=0, fill=0)

        # Fetch data
        info        = client.fetch()
        state       = info['state']
        eltime      = info['eltime']
        vol         = info['volume']
        artist      = info['artist']
        title       = info['title']
        audio       = info['audio_info']
        hostname    = info['hostname']
        hostip      = info['hostip']
        
        # Position text of Artist
        artwd,artz = draw.textsize(unicode(artist), font=font_artist)

	# Artist animate
	if artwd < width:
            artx = (width - artwd) / 2
	    artoffset = padding
        else:
            artx = artoffset
            #artoffset -= animate
            #if (artwd - (width + abs(artx))) < -120:
            #    artoffset = 100

        # Position text of Title
        titwd,titz = draw.textsize(unicode(title), font=font_title)

	# Title animate
	if titwd < width:
            titx = (width - titwd) / 2
	    titoffset = padding
        else:
            titx = titoffset
            titoffset -= animate
	    if (titwd - (width + abs(titx))) < -120:
		titoffset = 100

        # Position text of audio infomation
        audiox,audioy = draw.textsize(audio, font=font_info)
        if audiox < 126:
            audiox,audioy = divmod((126-audiox),2)
        else:
            audiox = 2

        if state == 'stop':
            # Draw text
            draw.text((35,top), hostname, font=font_artist, fill=255)
            draw.text((20,20), hostip, font=font_time, fill=255)
            draw.text((audiox,35), "", font=font_title, fill=255)
            draw.text((padding,45), "Stopped", font=font_time, fill=255)
            draw.text((75,45), "vol: " +  str(vol) , font=font_time, fill=255)
        else:
            # Draw text.
            draw.text((artx,top), unicode(artist), font=font_artist, fill=255)
            draw.text((titx,20), unicode(title), font=font_title, fill=255)
            draw.text((audiox,35), audio, font=font_info, fill=255)
            draw.text((padding,45), eltime, font=font_time, fill=255)
            draw.text((75,45), "vol: " +  str(vol) , font=font_time, fill=255)

        # Draw the image buffer.
        disp.image(image)
        disp.display()
        
        # Pause briefly before drawing next frame.
        time.sleep(0.7)

if __name__ == "__main__":
    main()