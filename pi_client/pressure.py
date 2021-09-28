"""
All of the code here is my own -R
Varun helped me understand the pin configuration and wrote the original design
However, I encapsulated it in order to keep things clean.

-D forgot the base specs for each of the sensors but pretty sure this one has a .2 N to 20 N trigger range
it'll be placed under the rock and if the rock is off then the pressure change? not the lack of pressure triggers it.
"""

from http_reqs import RequestMaker, defaultMaker
from helper import BaseSensor
import RPi.GPIO as GPIO
from asyncio import sleep
import time


# pin = 24
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(pin, GPIO.IN)

class PressureSensor(BaseSensor):

    # constructor.
    def __init__(self, mode, setup, pin: int):

        # super initialization.
        super().__init__(mode, setup, pin)
        self.last_input = 0

    def __enter__(self):
        # do nothing here, disabled by default.
        pass

    # enable sensor. Check if already enabled to avoid extraneous calls to pressure_check.
    def enable_sensor(self):
        if not self.enabled:
            self.enabled = True
            self.sensor_event = self.loop.run_in_executor(None, self.pressure_check)

    # disable sensor. Check if already disabled to avoid calls on NoneTypes.
    def disable_sensor(self):
        if self.enabled:
            self.enabled = False
            self.sensor_event.cancel()

    # Callback that GPIO can use.
    def callback(self, type: int):

        # int to boolean: python handles bools as 0 or 1. 1 = true, 0 = false.
        if type:
            #defaultMaker.discord_report(json={"content": message})
            result = ("pressure", "report", "Pressure not detected")
            defaultMaker.ws_server_report(*result)
        else:
            result = ("pressure", "report", "Pressure applied")
            defaultMaker.ws_server_report(*result)

    # only call callback if input != previous input.
    # checks for pressure.
    def pressure_check(self):
        while self.enabled:
            input = GPIO.input(self.pin)
            if (self.last_input != input):
                self.callback(input)
            self.last_input = input
            time.sleep(0.1)
