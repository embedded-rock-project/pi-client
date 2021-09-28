from helper import *
from pi_client import *
from config import *
from http_reqs import *

import nest_asyncio
nest_asyncio.apply()
from http_reqs import defaultMaker
import asyncio


import time
import json
import traceback


async def main():
    new_loop = asyncio.new_event_loop()
    cam = Camera(2, loop=new_loop)
    ms = MotionSensor(GPIO.BCM, GPIO.IN, 23)
    ps = PressureSensor(GPIO.BCM, GPIO.IN, 24)
    ds = DistanceSensor(GPIO.BCM, (18, GPIO.OUT), (25, GPIO.IN))

    last_msg = None 
    with ms, ps, cam:
        async for msg in defaultMaker.ws_server_listen():
            if not msg.data:
                break
            msg = json.loads(msg.data)
            if last_msg == msg:
                continue
            last_msg = msg
            

            sensor = msg["sensor"]
            isOn = msg["isSensorOn"]
            mode = msg["mode"]
            selection = {
                "camera": lambda mode: cam.switch_camera_mode(mode),
                "motion": lambda mode: ms.enable_sensor() if mode else ms.disable_sensor(),
                "pressure": lambda mode: ps.enable_sensor() if mode else ps.disable_sensor(),
                "distance": lambda mode: ds.enable_sensor() if mode else ds.disable_sensor()
            }
            if isOn and mode in [0, 1, 2]:
                selection.get(sensor, lambda mode: print("Invalid sensor: {}\nMode: {}".format(sensor, mode)))(mode)
            elif isOn:
                selection.get(sensor, lambda sensor: print("Invalid sensor: {}".format(sensor)))(sensor)

            elif not isOn:
                selection = {
                    "camera": lambda: cam.disable_camera(),
                    "motion": lambda: ms.disable_sensor(),
                    "pressure": lambda: ps.disable_sensor(),
                    "distance": lambda: ds.disable_sensor()

                }
                selection.get(sensor, lambda: print("Invalid sensor: {}".format(sensor)))()
            else:
                print(bool(isOn), bool(mode in [0, 1, 2]))



if (__name__ == "__main__"):
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    except Exception as e:
        traceback.print_exc()
    finally:
        defaultMaker.close()
        loop.close()