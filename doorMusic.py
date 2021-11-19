import RPi.GPIO as GPIO #refers to the pins on the PI
#import pygame.mixer #imports the pygame module to play music
from playsound import playsound
import multiprocessing
import time

musicThread=multiprocessing.Process(target=playsound, args=("Adele - Hello.mp3",))

def activeSetup():
    global active #this function creates a variable named active to decide
    active=0 #whether the system is active or not
    print("Currently Not Active") #sets active equal to zero
def activeState():
    global active #this function checks if the system is active
    if active==1: #if active, sets the system to inactive, turns off the
        active=0 #LED light and prints to the console
        GPIO.output(7, GPIO.LOW)
        print("Currently Not Active")
    elif active==0: #if inactive: gives you 10sec to close circuit, during which the light flashes
        print("Activating in 5 seconds") #before remaining on to show system is active
        for x in range(0, 5):
            GPIO.output(7, GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(7, GPIO.LOW)
            time.sleep(0.5)
        active=1
        GPIO.output(7, GPIO.HIGH)
        print("Currently Active")
    else: return

def watchDoor():
    global musicThread
    global active
    global playing #variable to prevent the program from attempting to

    playing = False #play repeatedly when switch triggered
    print("In watch door", active)
    while True:
        if active==1 and GPIO.input(15)==1 and playing==False: #plays music if system is active,
            playing=True #reed open, and isn't already playing
            musicThread.start()
            active=0
            print(active)

        if GPIO.input(13)==1:
            print("Stop button pressed: Exiting")
            musicThread.terminate()
            break
        
        if (GPIO.input(15)==0 and active==0): #push the button to stop music and exit program
            print("Door Closed")
            musicThread.terminate()
            active=1
            playing=False
            musicThread=multiprocessing.Process(target=playsound, args=("Adele - Hello.mp3",))
            
        if GPIO.input(11)==1: #to determine if system active or not
            activeState()
            time.sleep(0.5)
                


GPIO.setmode(GPIO.BOARD) #sets up Pi's pin connections
#GPIO.setwarnings(False)
GPIO.setup(7, GPIO.OUT, initial=GPIO.LOW) #initializes the arguement to low to start
GPIO.setup(11, GPIO.IN)
GPIO.setup(13, GPIO.IN)
GPIO.setup(15, GPIO.IN)

activeSetup()
#pygame.mixer.init(44100, -16, 2, 516) #initiates the Pygame mixer & is a buffer to control the latency the music
#pygame.mixer.music.set_volume(2.0) #is played
#name = "Adele - Hello.mp3"
#pygame.mixer.music.load(name)
#print("Loadedtrack - " + str(name))

while True: #waits for an input from either button, & quits or changes the state to active accordingly
    if(GPIO.input(13)==1):
        print("Stop button pressed: Exiting")
        musicThread.terminate()
        break
    if(GPIO.input(11)==1):
        activeState()
        time.sleep(0.5)
    if(active==1): #if active then watchDoor function activated and tune will play when door opened
        watchDoor()
        break
GPIO.cleanup() #resets pins
