import cv2
import numpy as np
import os
import pygame
import pygame.mixer
import time,datetime
import random
import telepot
from telepot.loop import MessageLoop

pygame.mixer.init()
pygame.mixer.music.load("/home/pi/Music/magic_gun (online-audio-converter.com).wav")
#initialize speaker
switch=True
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);
font = cv2.FONT_HERSHEY_SIMPLEX
#iniciate id counter
id = 0
# names related to ids: example ==> Marcelo: id=1,  etc
names = ['None', 'Eric', 'Paula', 'Ilza', 'Z', 'W'] 
# Initialize and start realtime video capture
cam = cv2.VideoCapture(0)
cam.set(3, 640) # set video widht
cam.set(4, 480) # set video height
# Define min window size to be recognized as a face
minW = 0.1*cam.get(3)
minH = 0.1*cam.get(4)


def action(msg):
    chat_id=msg['chat']['id']
    command=msg['text']
    
    print('Received: %s' % command)

    if 'Start' in command:
        message="Ok,sir!"
        telegram_bot.sendMessage(chat_id,message)
        
    if 'Add new face' in command:
        message="Please face the camera with your front face"
        telegram_bot.sendMessage(chat_id,message)
        
    
    #ask bot to open camera
    if 'Camera' in command:
        while switch==True:
            ret, img =cam.read()
            img = cv2.flip(img, -1) # Flip vertically
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            
            faces = faceCascade.detectMultiScale( 
                gray,
                scaleFactor = 1.2,
                minNeighbors = 5,
                minSize = (int(minW), int(minH)),
               )
            for(x,y,w,h) in faces:
                #random number for stranger's photo
                a=str(random.randrange(1,1000))
                cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
                id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
                # Check if confidence is less them 100 ==> "0" is perfect match 
                if (confidence < 55):
                    id = "Hello"
                    confidence = "  {0}%".format(round(100 - confidence))
                else:
                    id = "unknown"
                    confidence = "  {0}%".format(round(100 - confidence))
                    
                    #save photo to strangert folder
                    cv2.imwrite("stranger/dog."+a+".jpg",gray[y:y+h,x:x+w])
                    #send photo to telegram bot
                    stranger_path="/home/pi/FacialRecognitionProject/stranger/dog."+a+".jpg"
                    telegram_bot.sendPhoto(chat_id,photo=open(stranger_path,'rb'))
                    telegram_bot.sendMessage(chat_id,"There is a stranger outside your door!!")
                    
                    #play sound effect
                    pygame.mixer.music.play()
                    time.sleep(5)
                    
                cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
                cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)  
            
            cv2.imshow('camera',img) 
            k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
            if k == 27:
                break
            
            @run_async
            def stop(msg):
                chat_id=msg['chat']['id']
                command=msg['text']
                if 'Stop' in command: 
                    print("\n [INFO] Stop Camera and cleanup stuff")
                    cam.release()
                    cv2.destroyAllWindows()
                    switch=False
        
            
            
telegram_bot = telepot.Bot('5086512542:AAE1VaGpLrY1GFZV2u5rrEoPiW8RIBbLESE')
print (telegram_bot.getMe())
    
MessageLoop(telegram_bot, action).run_as_thread()
print('Up and Running....')

while 1:
    time.sleep(10)
    
    
# Do a bit of cleanup
#print("\n [INFO] Exiting Program and cleanup stuff")
#cam.release()
#cv2.destroyAllWindows()

