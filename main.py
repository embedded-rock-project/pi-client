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
import traceback


async def main():
    cam = Camera(2)
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
            mode = msg["mode"]
            sensor = msg["sensor"]
            if mode or mode == 0:
                selection.get(sensor, lambda mode: print("Invalid sensor: {}\nMode: {}".format(sensor, mode)))(mode)



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
        traceback.print_stack()
    finally:
        defaultMaker.close()
        loop.close()