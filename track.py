from random import randint

import cv2
import numpy as np

# init part
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
hand_cascade = cv2.CascadeClassifier('Hand.Cascade.1.xml')

f = open('data.in','w')

def detect_faces(img, cascade):
    global mask, pastx, pasty, pastw, pasth,pastrot

    gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    coords = cascade.detectMultiScale(gray_frame, 1.3, 5)
    frame = 0
    if len(coords) >= 1:
        height, width, _ = img.shape
        for (x, y, w, h) in coords:
            f.write('face ' + str(320-x) + ' ' + str(210-y) + ' ' + str(w) + ' ' + str(h) + '\n')
            print('face ' + str(320 - x) + ' ' + str(210 - y) + ' ' + str(w) + ' ' + str(h) )
            frame = img[y:y + h, x:x + w]
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 2)
        #frame = drawImg(mask, img, x, y, w, h, rot)
    else:
        pass
        #frame = drawImg(mask, img, pastx, pasty, pastw, pasth, pastrot)
    return frame

def detect_hands(img, cascade):
    global mask, pastx, pasty, pastw, pasth,pastrot

    gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    coords = cascade.detectMultiScale(gray_frame, 1.3, 5)
    frame = 0
    if len(coords) >= 1:
        height, width, _ = img.shape
        for (x, y, w, h) in coords:
            if 320-x>0:
                side='left'
            else:
                side='right'
            f.write('hand ' + str(320-x) + ' ' + str(210-y) + ' ' + str(w) + ' ' + str(h) +' '+side+ '\n')
            print('hand ' + str(320 - x) + ' ' + str(210 - y) + ' ' + str(w) + ' ' + str(h) + ' ' + side)
            frame = img[y:y + h, x:x + w]
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    else:
        pass
        #frame = drawImg(mask, img, pastx, pasty, pastw, pasth, pastrot)
    return frame


def detect_eyes(img, cascade):
    gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    eyes = cascade.detectMultiScale(gray_frame, 1.3, 5)  # detect eyes
    width = np.size(img, 1)  # get face frame width
    height = np.size(img, 0)  # get face frame height
    left_eye = None
    right_eye = None
    for (x, y, w, h) in eyes:
        if y > height / 2:
            pass
        eyecenter = x + w / 2  # get the eye center
        if eyecenter < width * 0.5:
            left_eye = img[y:y + h, x:x + w]
        else:
            right_eye = img[y:y + h, x:x + w]
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 255), 2)
    return left_eye, right_eye


def cut_eyebrows(img):
    height, width = img.shape[:2]
    eyebrow_h = int(height / 4)
    img = img[eyebrow_h:height, 0:width]  # cut eyebrows out (15 px)

    return img


def blob_process(img, threshold, detector):
    gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, img = cv2.threshold(gray_frame, threshold, 255, cv2.THRESH_BINARY)
    '''
    img = cv2.erode(img, None, iterations=2)
    img = cv2.dilate(img, None, iterations=4)
    img = cv2.medianBlur(img, 5)
    '''
    keypoints = detector.detect(img)
    if keypoints != ():
        print(keypoints)
    return keypoints


def nothing(x):
    pass


def main():
    global height, width, frame
    cap = cv2.VideoCapture(0)
    #cv2.namedWindow('image')
    #cv2.createTrackbar('threshold', 'image', 0, 255, nothing)
    _, frame = cap.read()
    height, width, _ = frame.shape
    print(f'{height},{width}')
    print('we open')
    while True:
        _, frame = cap.read()
        face_frame = detect_faces(frame, face_cascade)
        hand_frame = detect_hands(frame, hand_cascade)
        #cv2.imshow('image', frame)
        f.flush()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            f.close()
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
