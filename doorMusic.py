import RPi.GPIO as GPIO
import os
import random
from playsound import playsound #music functions
import multiprocessing#thread processes
import time#able to use counters and the current time with the next import
import datetime


def randomMusic():#function to choose music randomly from a folder
    randomSong = random.choice(os.listdir('/home/pi/DoorPi/musicFiles'))
    return randomSong 

print(randomMusic(), "Here")
musicThread = multiprocessing.Process(target= playsound, args=('musicFiles/' + randomMusic(),))#variables to call different musics
warningThread = multiprocessing.Process(target=playsound, args=("Kevin-Warning.mp3",))
   
def timeRange(start, end, current): #function to define time range for which music is played
    return start <= current <= end

start = datetime.time(1, 30, 0) #variables for time range
end = datetime.time(6, 00, 0)
current = datetime.datetime.now().time()
print(timeRange(start, end, current)) #print to test the range

def activeSetup():
    global active #this function creates a variable named active to decide whether the system is active or not
    active = 0
    print("Currently Not Active") #sets active equal to zero

def activeState():
    global active #this function checks if the system is active

    if active == 1: #if active, sets the system to inactive, turns off the LED light and prints to the console
        active = 0
        GPIO.output(7, GPIO.LOW)
        print("Currently Not Active")

    elif active == 0: #if inactive: gives you 5sec to close circuit, during which the light flashes
        print("Activating in 5 seconds") #before remaining on to show system is active
        for x in range(0, 5):
            GPIO.output(7, GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(7, GPIO.LOW)
            time.sleep(0.5)
        active = 1
        GPIO.output(7, GPIO.HIGH)
        print("Currently Active")
    else: return

def watchDoor(): #function to define if door is open or not and what to do
    global musicThread #calls the music variables into the function
    global warningThread
    global active
    global playing #variable to prevent the program from attempting to play repeatedly when switch triggered
    playing = False

    while True:
        if active == 1 and GPIO.input(15)==1 and playing==False: #plays music if system is active, reed open, & isn't already playing
            playing = True
            if(timeRange(start, end, current)): #if in time range, then plays burglar alarm
                warningThread.start()
                active = 0
                print(active)
            else: #else plays the fun music
                musicThread = multiprocessing.Process(target=playsound, args=('musicFiles/' + randomMusic(),))
                musicThread.start()
                active = 0
                print(active)

        if GPIO.input(13) == 1: #the off button to disarm the device
            print("Stop button pressed: Disarming")
            if(musicThread.is_alive() == True):
                musicThread.terminate()#this button disables the alarm
            if(warningThread.is_alive() == True):
                warningThread.terminate()
            active = 0
            loopingFun()
            break
        
        if (GPIO.input(15) == 0 and active == 0): #if door closed then stops music after 5 secs
            print("Door Closed")
            active = 1
            playing = False
            if(warningThread.is_alive() == True):
                time.sleep(8)
                warningThread.terminate()
                warningThread = multiprocessing.Process(target=playsound, args=("Kevin-Warning.mp3",))#indefinitably
            if(musicThread.is_alive() == True):
                time.sleep(5)
                musicThread.terminate()#resets both music variables tp allow the music to be played
                musicThread = multiprocessing.Process(target=playsound, args=('musicFiles/' + randomMusic(),))
        if GPIO.input(11) == 1: #to determine if system active or not
            activeState()
            time.sleep(0.5)

GPIO.setmode(GPIO.BOARD) #sets up Pi's pin connections
GPIO.setup(7, GPIO.OUT, initial = GPIO.LOW) #initializes the arguement to low to start
GPIO.setup(11, GPIO.IN)
GPIO.setup(13, GPIO.IN)
GPIO.setup(15, GPIO.IN)

def loopingFun():
    GPIO.output(7, GPIO.LOW)
    print("in the fun loop")
    while True:#waits for an input from either button, & quits or changes the state to active accordingly
        if(GPIO.input(11) == 1):#push this button to active the alarm system
            activeState()
            time.sleep(0.5)
        if(active == 1): #if active then watchDoor function activated and tune will play when door opened
            watchDoor()
            break
activeSetup()
loopingFun()
GPIO.cleanup() #resets pins
