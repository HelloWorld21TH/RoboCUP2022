import zmq
import pygame

pygame.joystick.init()
dscreen = pygame.display.set_mode([240, 160])
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
JOY_EVENT = [pygame.JOYAXISMOTION,pygame.JOYBALLMOTION,pygame.JOYHATMOTION,pygame.JOYBUTTONUP,pygame.JOYBUTTONDOWN]
AXIS0,AXIS1 = 0,0
LAXIS = ""

context = zmq.Context()
#  Socket to talk to server
print("Connecting to hello world server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://192.168.240.30:5555") #This is your Raspberry pi IP

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.JOYAXISMOTION:
            if event.axis == 0: AXIS0 = event.value
            if event.axis == 1: AXIS1 = event.value
            #print("AXIS0",AXIS0)
            #print("AXIS1",AXIS1)
    
    if AXIS1 >= 1 : LAXIS = "BACKWARD" 
    elif AXIS1 <= -1 : LAXIS = "FOWARD"
    elif AXIS0 >= 1 : LAXIS = "RIGHT"
    elif AXIS0 <= -1 : LAXIS = "LEFT"
    elif AXIS1 == -0.003936887722403638 == AXIS0: LAXIS = "STOP"
    socket.send_string(LAXIS)
    print(f"Sent : {LAXIS}")
    message = socket.recv()
    print(f"Received reply [ {message} ]")



