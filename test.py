import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)#sets up the pin locations
GPIO.setup(7, GPIO.OUT)
GPIO.setup(11, GPIO.IN)
GPIO.setup(13, GPIO.IN)
GPIO.setup(15, GPIO.IN)
while True:
	GPIO.output(7, GPIO.HIGH)#turns on LED
	if(GPIO.input(11)==1):#prints to screen based on which button is pushed
		print("Button on GPIO 11")
		time.sleep(1)
	if(GPIO.input(13)==1):
		print("Button on GPIO 13")
		time.sleep(1)
	if(GPIO.input(15)==1):
		print("Button on GPIO 15")
		time.sleep(1)

GPIO.cleanup()

