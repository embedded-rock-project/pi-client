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

    def __enter__(self):
        self.enable_sensor()

    def callback(self, sensor_pin: int):
        defaultMaker.discord_report(json={"content": "Motion sensor detected movement!"})

    def enable_sensor(self):
        if (not self.enabled):
            self.enabled = True
            GPIO.add_event_detect(self.pin, GPIO.RISING, callback=self.callback)

    def disable_sensor(self):
        if (self.enabled):
            self.enabled = False
            GPIO.remove_event_detect(self.pin)
