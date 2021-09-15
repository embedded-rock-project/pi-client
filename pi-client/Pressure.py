from helper.base_sensor import BaseSensor
import RPi.GPIO as GPIO
import time
from ..helper import BaseSensor
from asyncio import sleep


# pin = 24
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(pin, GPIO.IN)

class PressureSensor(BaseSensor):
    def __init__(self, mode, setup, pin: int):
        super().__init__(mode, setup, pin)
        self.prev_input = 0
        self.sensor_event = self._nowait(self.pressure_check())


    async def callback(self, message):
        print(message)


    async def check_if_enabled(self):
        while True:
            if self.enabled and not bool(self.sensor_event):
                self.sensor_event = self._nowait(self.pressure_check())  
            elif not self.enabled and bool(self.sensor_event):
                self.sensor_event = None
            sleep(1)


    async def pressure_check(self):
        while self.enabled:
            input = GPIO.input(self.pin)
            if (prev_input != input):
                self.callback("hi there")
            prev_input = input
            time.sleep(0.10)
