import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")
GET = ""
while True:
    #  Wait for next request from client
    message = socket.recv()
    print(f"Received request: {message}")
    GET = message
    print(GET)
    socket.send_string("recived")