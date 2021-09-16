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
        self.name = "motion sensor" #debug
        self.detecting_movement = False
        self.event_task = None


    def __enter__(self):
        self.enabled = True
        self.event_task = self.loop.run_in_executor(None, self.check_if_enabled)

    def __exit__(self):
        GPIO.cleanup()
        self.event_task.cancel()


    def callback(self):
        print("hello")
        defaultMaker.discord_report(json={"content": "There was movement!"})

    def check_if_enabled(self):
        while True:
            if self.enabled and not self.detecting_movement:
                print("added listener")
                GPIO.add_event_detect(self.pin, GPIO.RISING, callback=self.callback)
                self.detect_movement = True
            elif not self.enabled and self.detecting_movement:
                print("removed listener")
                GPIO.remove_event_detect(self.pin)
                self.detect_movement = False
            time.sleep(1)
