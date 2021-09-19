"""
All of the code here is my own -R
Varun helped me understand the pin configuration and wrote the original design
However, I encapsulated it in order to keep things clean.
"""

from http_reqs import RequestMaker, defaultMaker
from helper.base_sensor import BaseSensor
import RPi.GPIO as GPIO
from asyncio import sleep
import time


# pin = 24
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(pin, GPIO.IN)

class PressureSensor(BaseSensor):
    def __init__(self, mode, setup, pin: int):
        super().__init__(mode, setup, pin)
        self.last_input = 0

    def __enter__(self):
        self.enabled = True
        self.sensor_event = self.loop.run_in_executor(None, self.pressure_check)

    def enable_sensor(self):
        if not self.enabled:
            self.enabled = True
            self.sensor_event = self.loop.run_in_executor(None, self.pressure_check)

    def disable_sensor(self):
        if self.enabled:
            self.enabled = False
            self.sensor_event.cancel()

    def callback(self, message: str):
        defaultMaker.ws_server_report(message)

    def pressure_check(self):
        while self.enabled:
            input = GPIO.input(self.pin)
            if (self.last_input != input):
                self.callback("Pressure sensor detected pressure!")
            self.last_input = input
            time.sleep(0.1)
