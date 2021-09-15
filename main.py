from helper import *
from pi_client import *
from config import *
from http_reqs import *


import asyncio
import RPi.GPIO as GPIO

def main():
    ps = PressureSensor(GPIO.BCM, GPIO.IN, 24)
    ms = MotionSensor(GPIO.BCM, GPIO.IN, 23)
    with ps, ms:
        print(ps.name, ms.name)


if __name__ == "__main__":
    main()






# """
# Client side interactions with sensors and server.
# All interactions must be handled inside the code itself, 
# then data is handed off to a server to process.
# """


# import asyncio
# import helper
# from inherits import RequestMaker





# def main():
#     rm = RequestMaker()
#     emb = helper.build_embed("hi", fields=(("hi", "hi", False)))
#     emb_json = helper.embeds_to_json(emb)
#     resp = rm.handle_request_text(rm.request("POST", "https://httpbin.org/anything", json={"content": None, "embeds": emb_json}))
#     print(emb_json)
#     print(resp)
#     return



# if __name__ == "__main__":
#     main()
