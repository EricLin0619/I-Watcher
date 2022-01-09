# IOT-
# **I-watcher — I’m watching you**
---
Made by 資管3A林冠廷

# Overview
---
## Why I want to do this project ?

It is quite troublesome to take out the key from the bag to open the door every time I go home. Especially when I just came home from shopping. My hands were full but I still need to find out the key from my bag.  I wish the door could open by itself every time. So i want to make a machine that can open the door just by my face. Then I’ll never have to find the key to open the door anymore.

On the other hand, if relatives and friends visit my home, the host can also control the door lock directly through Telegram bot without opening the door personally.

## How to use this machine ?

1. First of all, you have to download telegram, a communication APP. Then establish a connection with I-Watcher , the bot on telegram.
2. Second, type in “Add new face” in the chat box,  and the camera will turn on to try to capture your face. Please use it in a place with sufficient light sources, otherwise the machine can’t find the face. After capturing the face, I-Watcher will tell you that your face has been stored.
3. Third, type in "Train" in the chat box to train a new face recognition model. After training, I-Watcher will tell you that your face has been trained.
4. Now, we can start using facial recognition to unlock the door! Type in “Turn on the camera” to turn on the pi camera, then camera will turn on and start to recognize face. 
    1. If I-Watcher recognizes your face, I-Watcher will unlock the door for five seconds and play a welcome home sound effect. Simultaneously，send a welcome home message in telegram. 
    2. If it cannot recognize your face, It will play a sound effect to warn the stranger. And take a photo of stranger and send it to the owner's mobile phone. Finally, the camera will be turned off automatically.

## Commands you can use in I-Watcher

- Start : to check if your bot wakeup
    - Reply : “Ok,sir!”
- Open the door : to open the door lock
    - Reply : “Door’s been opened.”
- Close the door : to close the door
    - Reply : “Door’s been closed.”
- Add new face :
    - Reply1 : Please face the camera with your front face.
    - Reply2 : I've gotten your face!
- Train :
    - Reply1 : Ok, I'm training now. Wait a minute please.
    - Reply2 : I can recognize your face now!
- Turn on the camera :
    - Reply1 : Welcome home,my lord.
    - Reply2 : There is a stranger outside your door!!
    - Reply3 : The camera will be turned off in few seconds.

⚠️All the commands can only be used when camera is off.

## Feature list

1. Open the solenoid lock.
2. Close the solenoid lock.
3. Use pi camera to get new faces.
4. Train the facial recognition model.
5. Recognize the face in the database.
6. Make sound effect whether it detect the stranger or someone it know.
7. Send the stranger’s profile to the host’s mobile phone.
8. Do all the features above in telegram.

# Preparation
---
## Hardware

- Raspberry Pi 4 Model B
- Jumper Wire
- Solenoid lock (DC12V/0.8A )
- Relay 5V
- Speaker、audio cable
- Power supply (input 100~240V , output 12V )
- Pi camera

## Software

- Python 3.9.2
- Opencv 4.5.1
- Python Telegram Bot 12.7
- Pygame
- Telegram App
