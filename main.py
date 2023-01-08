#This code is a pwogram designed to cweate a virtuaw charactew that can bwink, twawk, and move its eyes based on the user's mouse position. It uses sewewaw wibraries, incwuding pygame, psutil, and pyaudio, to accompwish this. It awso wecords audio input and uses it to detewmine whethew the charactew is twawking ow not. owo

from random import randint
import pygame
import psutil
import pyaudio
import struct
import pyautogui
import math
import cv2
import sounddevice as sd
import numpy as np
position=0


print('hello') #Prints "hello"
print("ready") #Prints "ready"
pygame.init() #Initializes pygame
print('set') #Prints "set"
size = (500, 500) #Sets the size of the window
screen = pygame.display.set_mode(size) #Sets the window size
print('go') #Prints "go"
pygame.display.set_caption("Kit's shits") #Sets the window title
pygame.mixer.init() #Initializes the mixer
pygame.mixer.music.load("bink.mp3") #Loads the sound file

#Sets the initial values of the variables
talking = blinking= False
frames = []

#Sets the audio parameters
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "voice.wav"

p = pyaudio.PyAudio() #Initializes the pyaudio
volume = 0
threshold = 35
stream = p.open(format=FORMAT,channels=CHANNELS,rate=RATE,input=True,frames_per_buffer=CHUNK)

#Function to record audio
def record():
    global volume
    data = stream.read(CHUNK)
    volume = rms(data) * 10000
    print('|'*int(volume))

#Function to calculate the root mean square of the audio
def rms(data):
    count = len(data)/2
    format = "%dh"%(count)
    shorts = struct.unpack( format, data )
    sum_squares = 0.0
    for sample in shorts:
        # sample is a signed short in +/- 32768.
        # normalize it to 1.0
        n = sample * (1.0/32768.0)
        sum_squares += n*n

    return math.sqrt( sum_squares / count )

#Function to draw the eyes
def eye():
    pygame.draw.rect(screen, 'white',pygame.Rect(200,140,100,75))
    pygame.draw.ellipse(screen, (210,24,81), pygame.Rect((260+(position.x*0.008)-5, 160+(position.y*0.025)-10), (19, 27)))
    pygame.draw.ellipse(screen, (210,24,81),pygame.Rect((215 + (position.x * 0.008) - 5, 160 + (position.y * 0.025) - 10), (19, 27)))


done = False #Sets the done variable to false
clock = pygame.time.Clock() #Initializes the clock

kat = pygame.image.load('blinkclose.png') #Loads the image
up=0
wscale = kat.get_height() / kat.get_width() #Calculates the scale of the image

#Main loop
while not done:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
    if blinking: #Checks if the character is blinking
        if up==0: #Checks if the character is in the middle of a blink
            if "osu.exe" not in (i.name() for i in psutil.process_iter()) and randint(0,2)==1: #Checks if the game is running
                pygame.mixer.music.play() #Plays the sound
            up+=1 #Increments the up variable
        if randint(up,5) == 4: #Checks if the character is done blinking
            blinking = False #Sets the blinking variable to false
            up =0 #Resets the up variable
    else: #Checks if the character is not blinking
        if randint(0,100) == 49: #Checks if the character should start blinking
            blinking = True #Sets the blinking variable to true
            up=0 #Resets the up variable
    record() #Calls the record function

    if volume > threshold: #Checks if the volume is above the threshold
        talking = True #Sets the talking variable to true
    else:
        talking = False #Sets the talking variable to false

    if talking: #Checks if the character is talking
        if blinking: #Checks if the character is blinking
            kat = pygame.image.load('blinkopen.png') #Loads the blinking open image
        else:
            kat = pygame.image.load('open.png') #Loads the open image
    else: #Checks if the character is not talking
        if blinking: #Checks if the character is blinking
            kat = pygame.image.load('blinkclose.png') #Loads the blinking closed image
        else:
            kat = pygame.image.load('closed.png') #Loads the closed image

    position = pyautogui.position() #Gets the mouse position
    kat = pygame.transform.scale(kat,(400,400*wscale)) #Scales the image
    screen.fill('green') #Fills the screen with green
    if not blinking: #Checks if the character is not blinking
        eye() #Calls the eye function
    screen.blit(kat, (50, 250-200*wscale)) #Draws the image
    pygame.display.flip() #Updates the display
    clock.tick(30) #Sets the framerate

#Closes the audio stream
stream.stop_stream()
stream.close()
p.terminate()
pygame.quit() #Closes the window