import math
import struct
import subprocess
import wave
import cv2
import numpy as np
import os
from tkinter import filedialog
import moviepy.editor as mp
from moviepy.editor import *
from pydub import AudioSegment
import soundfile as sf
face = cv2.imread("face.png")

print('hewwo! imma ask you to open some video files for me')
file_path= filedialog.askopenfilenames()
things=0
def rms(data):
    count = len(data) / 2
    sum_squares = 0.0
    for sample in data:
        n = sample * (1.0 / 32768.0)
        sum_squares += n * n
    return math.sqrt(sum_squares)

def detect_faces(img):
    global face
    cascades = [cv2.CascadeClassifier('haarcascade_frontalface_default.xml'),cv2.CascadeClassifier('haarcascade_frontalface_alt.xml'),cv2.CascadeClassifier('haarcascade_frontalface_alt.xml'),cv2.CascadeClassifier('haarcascade_profileface.xml')]
    frame = img
    for i in range(0,len(cascades)):
        cascade=cascades[i]
        gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        coords = cascade.detectMultiScale(gray_frame, 1.3, 5)
        if len(coords) >= 1:
            height, width, _ = img.shape
            for (x, y, w, h) in coords:
                frame = img[y:y + h, x:x + w]
            frame = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 2)
            frame = drawImg(frame, face, x, y, w, h)
            break
    return frame

def detect_hands(img):
    cascades = [cv2.CascadeClassifier('palm.xml'),
                cv2.CascadeClassifier('hand.xml'),
                cv2.CascadeClassifier('Hand.Cascade.1.xml')]
    frame = img

    for cascade in cascades:
        gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        coords = cascade.detectMultiScale(gray_frame, 1.3, 5)
        if len(coords) >= 1:
            height, width, _ = img.shape
            for (x, y, w, h) in coords:
                if 320-x>0:
                    side='left'
                else:
                    side='right'
                print(side+ ' hand located!')
                frame = img[y:y + h, x:x + w]
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return frame

def drawImg(frame,img,x,y,w,h):
    face =cv2.resize(img,(w+100,h+100))
    # Get the width and height of the face image
    face_h, face_w = face.shape[:2]

    # Specify the point to place the face image
    x_offset = x
    y_offset = y-50

    fheight,fwidth=frame.shape[:2]

    for j in range(h+100):
        for i in range(w+100):
            if face[i,j].any() and fwidth-1> j+y_offset  and j+y_offset>0 and fheight-1>i+x_offset and i+x_offset>0:
                try:
                    frame[i+x_offset,j+y_offset]=face[i,j]
                except Exception as e:
                    print(f'{e} at : frame[{i+x_offset},{j + y_offset}]=face[{i},{j}]')
                    break

    return frame

for file in file_path:
    path, ext = os.path.splitext(file)
    name = path.split('/')[-1]
    if ext == '.mp4' or ext == '.webm' or ext == '.avi':
        print('type: '+ext)
        video = cv2.VideoCapture(file)
        vclip = VideoFileClip(file)
        audio = vclip.audio
        tframes = video.get(cv2.CAP_PROP_FRAME_COUNT)
        print("we're starting on "+file)
        fps = video.get(cv2.CAP_PROP_FPS)
        #data,sr = sf.read(audio)
        frames = []
        volumes = []
        things+=1
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        fourccc = cv2.VideoWriter_fourcc(*'mp4a')
        filename = name + "+" +str(things) + '.mp4'
        framez=0
        while (video.isOpened()):
            _,frame = video.read()
            if _:
                volume=0
                try:
                    aframe = audio.to_soundarray(framez)
                    volume = rms(aframe)
                except:
                    pass
                print(str(round(framez/tframes*100,1))+"%\t"+'|'*int(framez/tframes*50))
                frame = detect_faces(frame)
                frame = cv2.putText(frame,str(volume),(50,50),cv2.FONT_HERSHEY_SIMPLEX,1, (255,255,255),2,cv2.LINE_AA)
                frames.append(frame)
                out = cv2.VideoWriter(filename, fourcc, fps, (frame.shape[1], frame.shape[0]))

                framez+=1
            else:
                break

        for fram in frames:
            out.write(fram)
        print('adding audio to '+name)
        out.release()

        temp = VideoFileClip(filename)
        vf = temp.set_audio(audio)
        filename = path + "+" + str(things) + '.mp4'
        vf.write_videofile(filename)

        print(name + " is done at "+ filename)



    else:
        print('Nigga you need to choose a video not whatever the hell '+ name+ ext+' is dawg')
        break
print("DONEEE")