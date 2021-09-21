# from helper import *
# from pi_client import *
# from config import *
# from http_reqs import *

import nest_asyncio
nest_asyncio.apply()

from pi_client import Camera
from http_reqs import defaultMaker
import asyncio


import time
import json
import traceback


async def main():
    new_loop = asyncio.new_event_loop()
    cam = Camera(2, loop=new_loop)
    #ms = MotionSensor(GPIO.BCM, GPIO.IN, 23)
    with cam:
        async for msg in defaultMaker.ws_server_listen():
            if not msg.data:
                break
            msg = json.loads(msg.data)
            selection = {
                "camera": lambda mode: cam.switch_camera_mode(mode),
               #"motion": lambda mode: ms.enable_sensor() if mode else ms.disable_sensor()
            }
            sensor = msg["sensor"]
            isOn = msg["isSensorOn"]
            mode = msg["mode"]
            if isOn and mode in [0, 1, 2]:
                selection.get(sensor, lambda mode: print("Invalid sensor: {}\nMode: {}".format(sensor, mode)))(mode)
            elif isOn:
                selection.get(sensor, lambda mode: print("Invalid sensor: {}\nMode: {}".format(sensor, cam.camera_mode_choice)))(cam.camera_mode_choice)

            elif not isOn:
                selection = {
                    "camera": lambda: cam.disable_camera(),
                    #"motion": lambda: ms.disable_sensor(),
                }
                selection.get(sensor, lambda: print("Invalid sensor: {}".format(sensor)))()



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
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    except Exception as e:
        traceback.print_exc()
    finally:
        defaultMaker.close()
        loop.close()