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


    def __enter__(self):
        self.enabled = True
        self.check_if_enabled()


    def callback(self):
        defaultMaker.discord_report(json={"content": "There was movement!"})

    def check_if_enabled(self):
        while True:
            if self.enabled and not self.detecting_movement:
                print("hi")
                GPIO.add_event_detect(self.pin, GPIO.RISING, callback=self.callback)
                self.detect_movement = True
            elif not self.enabled and self.detecting_movement:
                GPIO.remove_event_detect(self.pin)
                self.detect_movement = False
            time.sleep(1)
