import RPi.GPIO as GPIO
import time
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

#STB PWM ON
GPIO.output(32, 1)
GPIO.output(38, 1)
GPIO.output(40, 1)
GPIO.output(36, 1)

#Servo
SList = 1
ServoAngle = [0,0,0,0,0,0]

GPIO.setup(3, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(7, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)

Servo1 = GPIO.PWM(3, 50) # GPIO 17 for PWM with 50Hz
Servo2 = GPIO.PWM(5, 50)
Servo3 = GPIO.PWM(7, 50)
Servo4 = GPIO.PWM(11, 50)
Servo5 = GPIO.PWM(13, 50)
Servo6 = GPIO.PWM(15, 50)

SerList = [Servo1,Servo2,Servo3,Servo4,Servo5,Servo6]

Servo1.start(2.5) # Initialization
Servo2.start(2.5)
Servo3.start(2.5)
Servo4.start(2.5)
Servo5.start(2.5)
Servo6.start(2.5)


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

def Angle(angle):
    duty = angle / 18 + 2
    return duty

def ServoPOS(x):
    if x > 6 : x = x-6
    elif x < 1 : x = 6-x
    return x

def ServoAPOS(x):
    if x > 180 : x = x-180
    elif x < 1 : x = 180-x
    return x

try:
    while(1):
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
        elif message ==  b'A':
            print("Left")
            Motor(-100,100)
        elif message ==  b'S':
            print("Backward")
            Motor(-100,-100)
        elif message ==  b'D':
            print("Right")
            Motor(100,-100)

        elif message ==  b'LEFT':
            print("Servo Previous")
            SList -= 1
            SList = ServoPOS(SList)
            print(SList)
            print(SerList[SList-1])
        elif message ==  b'RIGHT':
            print("Servo Next")
            SList += 1
            SList = ServoPOS(SList)
            print(SList)
            print(SerList[SList-1])
        elif message ==  b'UP':
            ServoAngle[SList-1] += 10
            ServoAngle[SList-1] = ServoAPOS(ServoAngle[SList-1])
            SerList[SList-1].ChangeDutyCycle(Angle(ServoAngle[SList-1]))
            print(ServoAngle)
            print(SList)
        elif message ==  b'DOWN':
            ServoAngle[SList-1] -= 10
            ServoAngle[SList-1] = ServoAPOS(ServoAngle[SList-1])
            SerList[SList-1].ChangeDutyCycle(Angle(ServoAngle[SList-1]))
            print(ServoAngle)
            print(SList)

    GPIO.cleanup()

except KeyboardInterrupt:
  GPIO.cleanup()