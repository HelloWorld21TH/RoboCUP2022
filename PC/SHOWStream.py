import cv2
import imagezmq
image_hub = imagezmq.ImageHub()
while True:  # show streamed images until Ctrl-C
    rpi_name, image = image_hub.recv_image()
    resized = cv2.resize(image, (900,750), interpolation = cv2.INTER_AREA)
    cv2.imshow(rpi_name, resized) # 1 window for each RPi
    cv2.waitKey(1)
    image_hub.send_reply(b'OK')