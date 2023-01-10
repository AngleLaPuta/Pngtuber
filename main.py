# This code is a pwogram designed to cweate a virtuaw charactew that can bwink, twawk, and move its eyes based on the user's mouse position. It uses sewewaw wibraries, incwuding pygame, psutil, and pyaudio, to accompwish this. It awso wecords audio input and uses it to detewmine whethew the charactew is twawking ow not. owo

from random import randint
from configparser import ConfigParser
import pygame
import psutil
import pyaudio
import struct
import pyautogui
import math
import cv2
import sounddevice as sd
import numpy as np

position = 0
f = open('/dist/data.txt', 'r+')
configur = ConfigParser()
configur.read('config.ini')
print("Sections : ", configur.sections())
print("ready")  # Prints "ready"
pygame.init()  # Initializes pygame
print('set')  # Prints "set"
size = (int(configur.get('window', 'x')), int(configur.get('window', 'y')))  # Sets the size of the window
screen = pygame.display.set_mode(size)  # Sets the window size
print('go')  # Prints "go"
pygame.display.set_caption(configur.get('window', 'title'))  # Sets the window title
pygame.mixer.init()  # Initializes the mixer
pygame.mixer.music.load("bink.mp3")  # Loads the sound file

talks = configur.getboolean('features', 'talks')
blinks = configur.getboolean('features', 'blinks')
tab = configur.getboolean('features', 'tablet')
rat = configur.getboolean('features', 'mouse')

# Sets the initial values of the variables
talking = blinking = False
frames = []
data_dict = {}

# Sets the audio parameters
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "voice.wav"

try:
    eyecolor = tuple(map(int, configur.get('eyes', 'color').split(',')))
except:
    eyecolor = configur.get('eyes', 'color')

rightx = configur.getint('eyes', 'rightx')
righty = configur.getint('eyes', 'righty')
leftx = configur.getint('eyes', 'leftx')
lefty = configur.getint('eyes', 'lefty')
sens = float(configur.get('window', 'sens'))

p = pyaudio.PyAudio()  # Initializes the pyaudio
volume = 0
threshold = int(configur.get('sound', 'threshold'))
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)


# Function to record audio
def record():
    global volume
    data = stream.read(CHUNK)
    volume = rms(data) * 10000
    print('|' * int(volume))


def fill():
    global data_dict
    data = f.readlines()
    data_dict = {}
    # parse the data
    for line in data:
        line_list = line.split()
    if line_list[0] == 'face':
        data_dict['face'] = {'x': int(line_list[1]), 'y': int(line_list[2]), 'w': int(line_list[3]),'h': int(line_list[4])}
    elif line_list[0] == 'hand':
        data_dict['hand'] = {'x': int(line_list[1]), 'y': int(line_list[2]), 'w': int(line_list[3]),'h': int(line_list[4]),'facing':int(line_list[5])}
    f.truncate(0)

# Function to calculate the root mean square of the audio
def rms(data):
    count = len(data) / 2
    format = "%dh" % (count)
    shorts = struct.unpack(format, data)
    sum_squares = 0.0
    for sample in shorts:
        # sample is a signed short in +/- 32768.
        # normalize it to 1.0
        n = sample * (1.0 / 32768.0)
        sum_squares += n * n

    return math.sqrt(sum_squares / count)


# Function to draw the eyes
def eye():
    pygame.draw.rect(screen, 'white', pygame.Rect(200, 140, 100, 75))
    pygame.draw.ellipse(screen, eyecolor, pygame.Rect(
        (leftx + (position.x * 0.016 / sens) - 10 / sens, lefty + (position.y * 0.025 / sens) - 10 / sens), (19, 27)))
    pygame.draw.ellipse(screen, eyecolor, pygame.Rect(
        (rightx + (position.x * 0.016 / sens) - 10 / sens, righty + (position.y * 0.025 / sens) - 10 / sens), (19, 27)))
    

done = False  # Sets the done variable to false
clock = pygame.time.Clock()  # Initializes the clock

kat = pygame.image.load('blinkclose.png')  # Loads the image
up = 0
wscale = kat.get_height() / kat.get_width()  # Calculates the scale of the image

# Main loop
while not done:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop

    if blinks and blinking:  # Checks if the character is blinking
        if up == 0:  # Checks if the character is in the middle of a blink
            if "osu.exe" not in (i.name() for i in psutil.process_iter()) and randint(0,2) == 1:  # Checks if the game is running
                pygame.mixer.music.play()  # Plays the sound
            up += 1  # Increments the up variable
        if randint(up, 5) == 4:  # Checks if the character is done blinking
            blinking = False  # Sets the blinking variable to false
            up = 0  # Resets the up variable
    else:  # Checks if the character is not blinking
        if blinks and randint(0, 100) == 49:  # Checks if the character should start blinking
            blinking = True  # Sets the blinking variable to true
            up = 0  # Resets the up variable
    record()  # Calls the record function

    if talks and volume > threshold:  # Checks if the volume is above the threshold
        talking = True  # Sets the talking variable to true
    else:
        talking = False  # Sets the talking variable to false

    if talks and talking:  # Checks if the character is talking
        if blinking:  # Checks if the character is blinking
            kat = pygame.image.load('blinkopen.png')  # Loads the blinking open image
        else:
            kat = pygame.image.load('open.png')  # Loads the open image
    else:  # Checks if the character is not talking
        if blinking:  # Checks if the character is blinking
            kat = pygame.image.load('blinkclose.png')  # Loads the blinking closed image
        else:
            kat = pygame.image.load('closed.png')  # Loads the closed image

    try:
        rot = data_dict['x']/50
    except:
        rot =0
    position = pyautogui.position()  # Gets the mouse position
    kat = pygame.transform.scale(kat, (400, 400 * wscale))  # Scales the image
    if tab:
        tablet = pygame.image.load('Tablet.png')
        tablet = pygame.transform.scale(tablet, (400, 300))  # Scales the image
        drawhand = pygame.image.load('TabletHand.png')
        drawhand = pygame.transform.scale(drawhand, (200, 200))
    if rat:
        mouse = pygame.image.load('Mouse.png')
        mouse = pygame.transform.scale(mouse, (200, 200))
    screen.fill('green')  # Fills the screen with green
    if not blinking:  # Checks if the character is not blinking
        eye()  # Calls the eye function
    screen.blit(pygame.transform.image(kat,rot), (50, 250 - 200 * wscale))  # Draws the image
    if tab:
        screen.blit(drawhand,(0+position.x*0.18,140+position.y*0.1875))
        screen.blit(tablet, (10, 150))  # Draws the image
    if rat:
        screen.blit(mouse,(position.x*0.01*sens,300))
    pygame.display.flip()  # Updates the display
    clock.tick(30)  # Sets the framerate

# Closes the audio stream
stream.stop_stream()
stream.close()
p.terminate()
pygame.quit()  # Closes the window
