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
        self.name = "pressure sensor" # debug
        self.prev_input = 0
        self.event_task = None
        self.sensor_event = None


    def __enter__(self):
        self.enabled = True
        self.loop.run_in_executor(None, self.check_if_enabled)


    def __exit__(self, exc_type, exc_value, traceback):
        GPIO.cleanup()
        self.event_task.cancel()


    def callback(self, message: str):
        defaultMaker.discord_report(json={"content": message})


    def check_if_enabled(self):
        while True:
            if self.enabled and not bool(self.sensor_event):
                self.sensor_event = self._nowait(self.pressure_check())  
            elif not self.enabled and bool(self.sensor_event):
                self.sensor_event.cancel()
                self.sensor_event = None
            time.sleep(0.1)


    async def pressure_check(self):
        while self.enabled:
            input = GPIO.input(self.pin)
            if (self.prev_input != input):
                self.callback("There was pressure!")
            self.prev_input = input
            await sleep(0.10)
