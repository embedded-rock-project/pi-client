import RPi.GPIO as GPIO
import time
from http_reqs import defaultMaker
import asyncio


class DistanceSensor:
    def __init__(self, mode, pin_trigger, pin_echo, loop=None):
        self.enabled = False
        self.sensor_event = None
        self.pin_trigger_int = pin_trigger[0]
        self.pin_echo_int = pin_echo[0]
        GPIO.setmode(mode)  # GPIO.BOARD
        GPIO.setup(pin_trigger[0], pin_trigger[1])
        GPIO.setup(pin_echo[0], pin_echo[1])
        self.loop = loop if loop else asyncio.get_event_loop()

    def __enter__(self):
        self.enable_sensor()

    def __exit__(self, exc_type, exc_value, traceback):
        self.disable_sensor()
        GPIO.cleanup()

    def disable_sensor(self):
        if self.enabled:
            self.enabled = False
            self.sensor_event.cancel()

    def enable_sensor(self):
        if not self.enabled:
            self.enabled = True
            self.sensor_event = self.loop.run_in_executor(None, self.check_distance)

    def check_distance(self):
        while self.enabled:
            GPIO.output(self.pin_trigger_int, GPIO.LOW)
            time.sleep(2)
            GPIO.output(self.pin_trigger_int, GPIO.HIGH)
            time.sleep(0.00001)
            GPIO.output(self.pin_trigger_int, GPIO.LOW)
            while GPIO.input(self.pin_trigger_int) == 0:
                pulse_start_time = time.time()
            while GPIO.input(self.pin_trigger_int) == 1:
                pulse_end_time = time.time()
            pulse_duration = pulse_end_time - pulse_start_time
            distance = round(pulse_duration * 17150, 2)
            print("wtf")
            defaultMaker.discord_report(
                json={"content": f"Distance: {distance} cm"})
