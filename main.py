# from helper import *
# from pi_client import *
# from config import *
# from http_reqs import *

from pi_client import Camera
from http_reqs import defaultMaker
import asyncio
import nest_asyncio
nest_asyncio.apply()
import time
import json

async def main():
    cam = Camera(2)
    with cam:
        async for msg in defaultMaker.ws_server_listen():
            if not msg.data:
                break
            msg = json.loads(msg.data)
            test = msg.get('mode')
            if test or test == 0:
                cam.switch_camera_mode(test)


   # ps = PressureSensor(GPIO.BCM, GPIO.IN, 24)
   # ms = MotionSensor(GPIO.BCM, GPIO.IN, 23)
   # ds = DistanceSensor(GPIO.BCM, (4, GPIO.OUT), (17, GPIO.IN))
    # cam = Camera(2)
    # with cam: 
    #     time.sleep(120)
        # cam.switch_camera_mode(2)
        # time.sleep(120)
        # cam.switch_camera_mode(0)
        # time.sleep(1200)



if (__name__ == "__main__"):
    # try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
        loop.close()
    # except Exception as e:
    #     print(e)