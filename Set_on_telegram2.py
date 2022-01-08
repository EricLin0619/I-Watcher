import cv2
import numpy as np
import os
import pygame
import pygame.mixer
import time,datetime
import random
import telepot
from PIL import Image
from telepot.loop import MessageLoop
#import face_dataset_fun
#import face_training_fun

pygame.mixer.init()
pygame.mixer.music.load("/home/pi/Music/magic_gun (online-audio-converter.com).wav")
#initialize speaker
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
        message="Please face the camera with your front face."
        telegram_bot.sendMessage(chat_id,message)
        data_set()
    
    if 'Train' in command:
        message="Ok, I'm training now."
        telegram_bot.sendMessage(chat_id,message)
        train()

    
    #ask bot to open camera
    if 'Open camera' in command:
        while True:
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
        print("\n [INFO] Stop Camera and cleanup stuff")   
        cam.release()
        cv2.destroyAllWindows()
#getFace function        
def data_set():
    a=str(random.randrange(1,1000))
    print("\n [INFO] Initializing face capture. Look the camera and wait ...")
    # Initialize individual sampling face count
    count = 0
    while(True):
        ret, img = cam.read()
        img = cv2.flip(img, -1) # flip video image vertically
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)     
            count += 1
            # Save the captured image into the datasets folder
            cv2.imwrite("dataset/User." + a+ '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])
            cv2.imshow('image', img)
        k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
        if k == 27:
            break
        elif count >= 30: # Take 30 face sample and stop video
            break
    # Do a bit of cleanup
    print("\n [INFO] Exiting Program and cleanup stuff")
    cam.release()
    cv2.destroyAllWindows()

#train function
def train():
    path = 'dataset'
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    aceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml");
    # function to get the images and label data
    def getImagesAndLabels(path):
        imagePaths = [os.path.join(path,f) for f in os.listdir(path)]     
        faceSamples=[]
        ids = []
        for imagePath in imagePaths:
            PIL_img = Image.open(imagePath).convert('L') # convert it to grayscale
            img_numpy = np.array(PIL_img,'uint8')
            id = int(os.path.split(imagePath)[-1].split(".")[1])
            faces = aceCascade.detectMultiScale(img_numpy)
            for (x,y,w,h) in faces:
                faceSamples.append(img_numpy[y:y+h,x:x+w])
                ids.append(id)
        return faceSamples,ids
    print ("\n [INFO] Training faces. It will take a few seconds. Wait ...")
    faces,ids = getImagesAndLabels(path)
    recognizer.train(faces, np.array(ids))
    # Save the model into trainer/trainer.yml
    recognizer.write('trainer/trainer.yml') # recognizer.save() worked on Mac, but not on Pi
    # Print the numer of faces trained and end program
    print("\n [INFO] {0} faces trained. Exiting Program".format(len(np.unique(ids))))

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

