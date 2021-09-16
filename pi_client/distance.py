import RPi.GPIO as GPIO
import time
from http_reqs import defaultMaker
import asyncio



class DistanceSensor:
    def __init__(self, mode, pin_trigger, pin_echo, loop = None):
        self.enabled = False
        self.event_task = None
        self.sensor_event = None
        self.pin_trigger_int = pin_trigger[0]
        self.pin_echo_int = pin_echo[0]
        GPIO.setmode(mode) #GPIO.BOARD
        GPIO.setup(pin_trigger[0], pin_trigger[1])
        GPIO.setup(pin_echo[0], pin_echo[1])
        self.loop = loop if loop else asyncio.get_event_loop()
        self._sync_nowait = self.loop.run_in_executor



    def __enter__(self):
        self.enabled = True
        self.event_task = self._sync_nowait(None, self.check_if_enabled)


    def __exit__(self, exc_type, exc_value, traceback):
        GPIO.cleanup()  
        self.event_task.cancel()


    def check_if_enabled(self):
        while True:
            if self.enabled and not bool(self.sensor_event):
                self.sensor_event = self._sync_nowait(None, self.check_distance)
            elif not self.enabled and bool(self.sensor_event):
                self.sensor_event = None
            time.sleep(0.1)


    def check_distance(self):
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
        defaultMaker.discord_report(json={"content":f"Distance: {distance} cm"})