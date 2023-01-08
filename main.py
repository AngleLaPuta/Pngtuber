from random import randint
#from playsound import playsound
import pygame
import psutil
import pyaudio
import struct
import pyautogui
import math
import cv2
#from wavefile import WaveReader
import sounddevice as sd
import numpy as np
position=0


print('hello')
print("ready")
pygame.init()
print('set')
size = (500, 500)
screen = pygame.display.set_mode(size)
print('go')
pygame.display.set_caption("Kit's shits")
pygame.mixer.init()
pygame.mixer.music.load("bink.mp3")


talking = blinking= False
frames = []

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "voice.wav"

p = pyaudio.PyAudio()
volume = 0
threshold = 35
stream = p.open(format=FORMAT,channels=CHANNELS,rate=RATE,input=True,frames_per_buffer=CHUNK)

def record():
    global volume
    data = stream.read(CHUNK)
    volume = rms(data) * 10000
    print('|'*int(volume))
    #print(str(volume)+"\n")

def rms(data):
    count = len(data)/2
    format = "%dh"%(count)
    shorts = struct.unpack( format, data )

    # iterate over the block.
    sum_squares = 0.0
    for sample in shorts:
        # sample is a signed short in +/- 32768.
        # normalize it to 1.0
        n = sample * (1.0/32768.0)
        sum_squares += n*n

    return math.sqrt( sum_squares / count )

def eye():
    #pygame.draw.ellipse(screen,'pink',pygame.Rect((position.x*500/1250,position.y* 500/750),(15,20)))
    pygame.draw.rect(screen, 'white',pygame.Rect(200,140,100,75))
    pygame.draw.ellipse(screen, (210,24,81), pygame.Rect((260+(position.x*0.008)-5, 160+(position.y*0.025)-10), (19, 27)))
    #pygame.draw.ellipse(screen, 'green', pygame.Rect((250, 160), (19, 27)))
    pygame.draw.ellipse(screen, (210,24,81),pygame.Rect((215 + (position.x * 0.008) - 5, 160 + (position.y * 0.025) - 10), (19, 27)))

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

kat = pygame.image.load('blinkclose.png')
up=0
wscale = kat.get_height() / kat.get_width()

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
    if blinking:
        if up==0:
            if "osu.exe" not in (i.name() for i in psutil.process_iter()) and randint(0,2)==1:
                pygame.mixer.music.play()
            up+=1
        if randint(up,5) == 4:
            blinking = False
            up =0
    else:
        if randint(0,100) == 49:
            blinking = True
            up=0
    record()

    if volume > threshold:
        talking = True
    else:
        talking = False

    if talking:
        if blinking:
            kat = pygame.image.load('blinkopen.png')
        else:
            kat = pygame.image.load('open.png')
    else:
        if blinking:
            kat = pygame.image.load('blinkclose.png')
        else:
            kat = pygame.image.load('closed.png')




    position = pyautogui.position()





    kat = pygame.transform.scale(kat,(400,400*wscale))



    screen.fill('green')
    if not blinking:
        eye()
    screen.blit(kat, (50, 250-200*wscale))


    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(30)
stream.stop_stream()
stream.close()
p.terminate()