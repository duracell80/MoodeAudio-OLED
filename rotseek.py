from RPi import GPIO
from time import sleep
import os

clk = 25
dt = 8

GPIO.setmode(GPIO.BCM)
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

counter 		= 0
counterLast 		= 0
counterDirection 	= 0
clkLastState = GPIO.input(clk)

try:

        while True:
                clkState = GPIO.input(clk)
                dtState = GPIO.input(dt)

		if clkState != clkLastState:
                        if dtState != clkState:
                       		counter += 1
                        else:
				counter -= 1

                if counter < counterLast:
			counterDirection = -1
		if counter > counterLast:
			counterDirection = 1

		if counterDirection != 0:
			if counterDirection == 1:
				if(clkState == 1):
					os.system("mpc play & mpc next")
			else:
				if(clkState == 1):
					os.system("mpc play & mpc prev")



		clkLastState 		= clkState
		counterLast 		= counter
		counterDirection	= 0
		sleep(0.01)
finally:
        GPIO.cleanup()
