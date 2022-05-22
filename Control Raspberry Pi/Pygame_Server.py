import RPi.GPIO as GPIO
import pygame
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")
GET = ""

GPIO.setmode(GPIO.BOARD)

#Motor Pin

#Boost
GPIO.setup(23, GPIO.OUT)
GPIO.setup(29, GPIO.OUT)
#---PWM---
GPIO.setup(36, GPIO.OUT)


#Left A
GPIO.setup(31, GPIO.OUT)
GPIO.setup(33, GPIO.OUT)
#---PWM---
GPIO.setup(38, GPIO.OUT)


#Right B
GPIO.setup(35, GPIO.OUT)
GPIO.setup(37, GPIO.OUT)
#---PWM---
GPIO.setup(40, GPIO.OUT)


#STB
GPIO.setup(32, GPIO.OUT)

def Motor(Left,Right):
    if Left > 0 and Right > 0:
        print("Forward")
        #Left
        GPIO.output(31, 1)
        GPIO.output(33, 0)
        
        #Right
        GPIO.output(35, 1)
        GPIO.output(37, 0)
        

    elif Left < 0 and Right < 0:
        print("Backward")
        #Left
        GPIO.output(31, 0)
        GPIO.output(33, 1)
        
        #Right
        GPIO.output(35, 0)
        GPIO.output(37, 1)
        

    elif Left > 0 and Right < 0:
        print("Right")
        #Left
        GPIO.output(31, 1)
        GPIO.output(33, 0)
        
        #Right
        GPIO.output(35, 0)
        GPIO.output(37, 1)
        

    elif Left < 0 and Right > 0:
        print("Left")
        #Left
        GPIO.output(31, 0)
        GPIO.output(33, 1)
        
        #Right
        GPIO.output(35, 1)
        GPIO.output(37, 0)

    elif Left == 0 and Right == 0:
        print("STOP")
        #Left
        GPIO.output(31, 0)
        GPIO.output(33, 0)
        
        #Right
        GPIO.output(35, 0)
        GPIO.output(37, 0)
        

def Boost(x):
    if x == 1:
        GPIO.output(27, 1)
        GPIO.output(29, 0)
        
    elif x == -1:
        GPIO.output(27, 0)
        GPIO.output(29, 1)
        
    elif x == 0:
        GPIO.output(27, 0)
        GPIO.output(29, 0)
        

while(1):
    
    #STB PWM ON
    GPIO.output(32, 1)
    GPIO.output(38, 1)
    GPIO.output(40, 1)
    GPIO.output(36, 1)

    message = socket.recv()
    print(f"Received request: {message}")
    socket.send_string("recived")

    if message ==  b'ESC':
        print("Exit")
        break
    elif message ==  b'':
        print("STOP")
        Motor(0,0)
    elif message ==  b'W':
        print("Forward")
        Motor(100,100)
    elif message ==  b'D':
        print("Right")
        Motor(100,-100)
    elif message ==  b'A':
        print("Left")
        Motor(-100,100)
    elif message ==  b'S':
        print("Backward")
        Motor(-100,-100)
    

GPIO.cleanup()