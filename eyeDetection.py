import cv2
import numpy as np
#import picamera
import time

face_cascade = cv2.CascadeClassifier('/home/pi/Desktop/Detection/haarcascade_frontalface_default.xml')

eye_cascade = cv2.CascadeClassifier('/home/pi/Desktop/Detection/haarcascade_eye.xml')
#camera =  picamera.PiCamera()


cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 15)
while 1:
    ret, img = cap.read()
    #img = np.full((100,80,3), 12, np.uint8)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        eyeLength = len(eyes)
        print(eyeLength)
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
        if(len(eyes)  < eyeLength/2):
            print('no eyes!!!')
        else:
            print('eyes found')

    cv2.imshow('img',img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()



