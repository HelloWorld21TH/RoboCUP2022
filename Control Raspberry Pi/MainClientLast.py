import zmq
import pygame
import os

pygame.joystick.init()
dscreen = pygame.display.set_mode([240, 160])
os.putenv('SDL_VIDEODRIVER', 'fbcon')
pygame.display.init()
AXIS0,AXIS1 = 0,0
LAXIS = ""
key = ""
context = zmq.Context()
#  Socket to talk to server
print("Connecting to hello world server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://192.168.240.96:5555") #This is your Raspberry pi IP

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                key = "ESC"
                pygame.quit()
            elif event.key == pygame.K_w:
                key = "W" 
                print("Foward")
            elif event.key == pygame.K_a:
                key = "A"
                print("Left")
            elif event.key == pygame.K_s:
                key = "S"
                print("Backward")
            elif event.key == pygame.K_d:
                key = "D"
                print("Right")
            elif event.key == pygame.K_i:
                key = "I"
                print("Servo +")
            elif event.key == pygame.K_k:
                key = "K"
                print("Servo -")
            elif event.key == pygame.K_j:
                key = "J"
                print("Servo-Previous")
            elif event.key == pygame.K_l:
                key = "L"
                print("Servo-Next")
        elif event.type == pygame.KEYUP:
            key = ""

        socket.send_string(key)
        print(f"Sent : {key}")
        message = socket.recv()
        print(f"Received reply [ {message} ]")


        



