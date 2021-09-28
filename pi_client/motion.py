"""
All of the code here is my own -R
Varun helped me understand the pin configuration and wrote the original design
However, I encapsulated it in order to keep things clean.
"""


import RPi.GPIO as GPIO
from http_reqs import RequestMaker, defaultMaker
from asyncio import sleep
from helper.base_sensor import BaseSensor
import time


#pin = 23
#mode = GPIO.BCM
#setup = GPIO.IN

class MotionSensor(BaseSensor):
    def __init__(self, mode, setup, pin: int):
        super().__init__(mode, setup, pin)
        self.motion_count = 0

    def __enter__(self):
        pass

    def callback(self, sensor_pin: int):
        #defaultMaker.discord_report(json={"content": "Motion sensor detected movement!"})
        result = ("motion", "report", "Motion detected")
        defaultMaker.ws_server_report(*result)
        self.currently_motion += 1

    def enable_sensor(self):
        if (not self.enabled):
            self.enabled = True
            GPIO.add_event_detect(self.pin, GPIO.RISING, callback=self.callback)
            self.sensor_event = self.loop.run_in_executor(None, self.check)


    def disable_sensor(self):
        if (self.enabled):
            self.enabled = False
            GPIO.remove_event_detect(self.pin)
            if (self.sensor_event):
                self.sensor_event.cancel()
                self.sensor_event = None


    async def check(self):
        while self.enabled:
            start = self.motion_count
            await sleep(1)
            if self.motion_count == start:
                result = ("motion", "report", "Motion not detected")
                defaultMaker.ws_server_report(*result)
            
