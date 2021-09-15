from helper.base_sensor import BaseSensor
import RPi.GPIO as GPIO


class DistanceSensor(BaseSensor):
    def __init__(self, mode, setup, pin: int):
        super().__init__(mode, setup, pin)


    