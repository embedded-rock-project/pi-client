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

    # create new event loop for reports (to not block sensors/camera)
    new_loop = asyncio.new_event_loop()

    # Instantiate new sensor/camera classes.
    cam = Camera(2, loop=new_loop)
    ms = MotionSensor(GPIO.BCM, GPIO.IN, 23)
    ps = PressureSensor(GPIO.BCM, GPIO.IN, 24)
    ds = DistanceSensor(GPIO.BCM, (18, GPIO.OUT), (25, GPIO.IN))

    # define variable to check new message against for repeats.
    last_msg = None 

    # enter into sensors/camera, enabling them.
    with ms, ps, ds, cam:

        # use an asyncronhous generator to get messages as completed.
        async for msg in defaultMaker.ws_server_listen():

            # check for blank data (I.E. closing)
            if not msg.data:
                break

            # load into json format
            msg = json.loads(msg.data)

            # skip repeats
            if last_msg == msg:
                continue
        
            # set last message so repeats are validated next time
            last_msg = msg
            

            # parse message data
            sensor = msg["sensor"]
            isOn = msg["isSensorOn"]
            mode = msg["mode"]

            # define dict to use a jump table on (pythonic switch statement pre 3.10)
            selection = {
                "camera": lambda mode: cam.switch_camera_mode(mode),
                "motion": lambda mode: ms.enable_sensor() if mode else ms.disable_sensor(),
                "pressure": lambda mode: ps.enable_sensor() if mode else ps.disable_sensor(),
                "distance": lambda mode: ds.enable_sensor() if mode else ds.disable_sensor()
            }

            # check if sensor is on and mode value is correct
            if isOn and mode in [0, 1, 2]:
                
                # get sensor/camera function to run with a default value otherwise.
                selection.get(sensor, lambda mode: print("Invalid sensor: {}\nMode: {}".format(sensor, mode)))(mode)
            elif isOn:

                # if sensor is on but mode is invalid, display.
                print("Invalid mode. {}".format(mode))

            elif not isOn:

                # separate dict for disabling sensors/camera.
                selection = {
                    "camera": lambda: cam.disable_camera(),
                    "motion": lambda: ms.disable_sensor(),
                    "pressure": lambda: ps.disable_sensor(),
                    "distance": lambda: ds.disable_sensor()

                }
                selection.get(sensor, lambda: print("Invalid sensor: {}".format(sensor)))()

            # handle all other unknowns.
            else:
                print(bool(isOn), bool(mode in [0, 1, 2]))



# run this only if we enter python environment from this file.
if (__name__ == "__main__"):

    # run until interrupted.
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())

    # skip report for keyboard interrupt.
    except KeyboardInterrupt:
        pass

    # print unknown errors.
    except Exception as e:
        traceback.print_exc()

    # call these after all error handling completes.
    finally:

        # close asyncio loops.
        defaultMaker.close()
        loop.close()