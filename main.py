# from helper import *
# from pi_client import *
# from config import *
# from http_reqs import *

from pi_client import Camera

import asyncio
import time

def main():
   # ps = PressureSensor(GPIO.BCM, GPIO.IN, 24)
   # ms = MotionSensor(GPIO.BCM, GPIO.IN, 23)
   # ds = DistanceSensor(GPIO.BCM, (4, GPIO.OUT), (17, GPIO.IN))
    cam = Camera(2)
    with cam: #, cam:
        time.sleep(120)
        # cam.switch_camera_mode(2)
        # time.sleep(120)
        # cam.switch_camera_mode(0)
        # time.sleep(1200)



if (__name__ == "__main__"):
    main()