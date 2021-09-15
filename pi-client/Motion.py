from numbers import Number
import RPi.GPIO as GPIO
import time
from asyncio import sleep
from ..helper import BaseSensor


#pin = 23
#mode = GPIO.BCM
#setup = GPIO.IN

class MotionSensor(BaseSensor):
    def __init__(self, mode, setup, pin: int):
        super().__init__(mode, setup, pin)
        self.detecting_movement = False
        self._await(self.check_if_enabled())



    def callback(self, channel):
        print("There was a movement!")


    async def check_if_enabled(self):
        while True:
            if self.enabled and not self.detecting_movement:
                GPIO.add_event_detect(self.pin, GPIO.RISING, callback=self.detection)
                self.detect_movement = True
            elif not self.enabled and self.detecting_movement:
                GPIO.remove_event_detect(self.pin, GPIO.RISING)
                self.detect_movement = False
            sleep(1)
