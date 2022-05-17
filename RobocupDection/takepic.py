import re
import cv2
from time import sleep

cam = cv2.VideoCapture(0)

cv2.namedWindow("test")

img_counter = 0
sleep(1)
while True:
    ret, frame = cam.read()
    scale_percent = 60 # percent of original size
    width = int(frame.shape[1] * scale_percent / 100)
    height = int(frame.shape[0] * scale_percent / 100)
    dim = (width, height)

        # resize image
    resized = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)

    if not ret:
        print("failed to grab frame")
        break
    cv2.putText(resized,str(img_counter), (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.imshow("test", resized)

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    else:
        sleep(0.55)
        
        img_name = "pic/opencvframe{}.png".format(img_counter)
 
        cv2.imwrite(img_name, resized)
       
        print("{} written!".format(img_name))
        img_counter += 1

cam.release()

cv2.destroyAllWindows()
