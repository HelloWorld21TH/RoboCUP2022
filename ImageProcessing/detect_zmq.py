import argparse
from distutils.util import strtobool
from glob import glob

import cv2
from imutils import resize

from deep_hazmat import DeepHAZMAT, visualizer
import imagezmq

image_hub = imagezmq.ImageHub()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", type=int, help="k value in network optimizer", default=0)
    parser.add_argument("-min_confidence", type=float, default=0.8)
    parser.add_argument("-nms_threshold", type=float, default=0.3)
    parser.add_argument("-segmentation_enabled", type=strtobool, default=True)
    parser.add_argument("-net_dir", type=str, default='net')
    args = parser.parse_args()

    deep_hazmat = DeepHAZMAT(
        k=args.k,
        net_directory=args.net_dir,
        min_confidence=args.min_confidence,
        nms_threshold=args.nms_threshold,
        segmentation_enabled=args.segmentation_enabled,
    )

    while True:
        rpi_name, image = image_hub.recv_image()
        image = cv2.resize(image, (900,750), interpolation = cv2.INTER_AREA)
        cv2.imshow("Stream",image)
        image_hub.send_reply(b'OK')
        image = cv2.resize(image, (320,240), interpolation = cv2.INTER_AREA)
        visualizer.put_text(
            image=image,
            text=f'p={deep_hazmat.optimizer.p} q={deep_hazmat.optimizer.q} k={args.k}',
            x=10,
            y=10,
            scale=0.4,
            color=(0, 0, 0),
        )
        

        for hazmat in deep_hazmat.update(image):
            hazmat.draw(image=image, padding=0.1)
        image = cv2.resize(image, (900,750), interpolation = cv2.INTER_AREA)
        cv2.imshow('image', image)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break


if __name__ == "__main__":
    main()
