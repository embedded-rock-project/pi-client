import RPi.GPIO as GPIO
import asyncio
from typing import Optional

#basic script for any sensor. uses asyncio for event oriented triggers 
class BaseSensor:

    # Initialization.
    # Define necessary inputs that extended classes will require to function.
    def __init__(self, mode, setup, pin: int, loop: Optional[asyncio.AbstractEventLoop] = None):
        GPIO.setmode(mode)
        GPIO.setup(pin, setup) 
        self.pin = pin
        self.loop = loop if loop else asyncio.get_event_loop()
        self._await = self.loop.run_until_complete
        self._nowait = self.loop.create_task
        self.enabled = False
        self.sensor_event = None

    # default disable sensor. Only called if not overwritten.
    def disable_sensor(self):
        if (self.enabled):
            self.enabled = False
            if (self.sensor_event):
                self.sensor_event.cancel()

    # default enable sensor. Only called if not overwritten.
    def enable_sensor(self):
        if (not self.enabled):
            self.enabled = True

    # default exit. Only called if not overwritten.
    def __exit__(self, exc_type, exc_value, traceback):
        self.disable_sensor()
        GPIO.cleanup()

