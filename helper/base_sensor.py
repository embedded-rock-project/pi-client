import RPi.GPIO as GPIO
import asyncio
from typing import Optional


class BaseSensor:
    def __init__(self, mode, setup, pin: int, loop: Optional[asyncio.AbstractEventLoop] = None):
        GPIO.setmode(mode) #GPIO.BCM
        GPIO.setup(pin, setup) #GPIO.IN
        self.pin = pin
        self.loop = loop if loop else asyncio.get_event_loop()
        self._await = self.loop.run_until_complete
        self._nowait = self.loop.create_task
        self.enabled = True

    def __enter__(self):
        pass

    def disable_sensor(self):
        self.enabled = False

    def enable_sensor(self):
        self.enabled = True

    def __exit__(self, exc_type, exc_value, traceback):
        GPIO.cleanup()
