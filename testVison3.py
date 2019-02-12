#import methods
import cv2
import numpy as np
import time
import json
from gpiozero import LED, Button, Buzzer
import RPi.GPIO as GPIO
#import pigpio



#mapping
face_cascade = cv2.CascadeClassifier('/home/pi/Desktop/Detection/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('/home/pi/Desktop/Detection/haarcascade_eye.xml')

#varibles
beginingTime= time.time()
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 60)
bz = Buzzer(20)
button = Button(7)
red = LED(18)
yellow = LED(15)
green = LED(14)

#define methods
def testImage(beginingTime,eyesClosed):
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter("testData.avi", fourcc, 60, (int(720), int(480))) 
    if beginingTime+120 > time.time(): 
        beginingTime= time.time()
    ret,img = cap.read()
    checkImage(img,eyesClosed)
    testImage(beginingTime,eyesClosed)

def checkImage(img,eyesClosed):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)
    
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        roi_gray2 = gray[y:y+h, x:x+w] 
        eyes = eye_cascade.detectMultiScale(roi_gray2)
        
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
        
        green.on()
        
        if(len(eyes)<1):
            print("no eyes")
            #time.sleep(1) # wai
            print(eyesClosed)
            green.off()
            yellow.on()
            if eyesClosed > 3:
                bz.beep(0.0005,0.0005,3000, True)
                red.on()
                yellow.off()
                time.sleep(1.5)

                red.off()

                ret,img = cap.read()
                checkImage(img,eyesClosed+1)
                #checkImage(cap.read())#Sounds alarm
                #send sleep alarm
                
            else:
                ret,img = cap.read()
                checkImage(img,eyesClosed+1)
        else:
            print('eyes found')
            yellow.off()
            #green.on()
            ret,img = cap.read()
            checkImage(img, eyesClosed=0)
           
    cv2.imshow('img',img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        exit()

testImage(beginingTime,eyesClosed=0)

out.write
cap.release()
cv2.destroyAllWindows()
