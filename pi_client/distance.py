import RPi.GPIO as GPIO
import time
from http_reqs import defaultMaker



class DistanceSensor:
    def __init__(self, mode, pin_trigger: tuple[int, int], pin_echo: tuple[int, int]):
        self.enabled = False
        self.event_task = None
        self.sensor_event = None
        self.pin_trigger_int = pin_trigger[0]
        self.pin_echo_int = pin_echo[0]
        GPIO.setmode(mode) #GPIO.BOARD
        GPIO.setup(pin_trigger[0], pin_trigger[1])
        GPIO.setup(pin_echo[0], pin_echo[1])
        GPIO.output(pin_trigger[0], GPIO.LOW)
        time.sleep(2)
        GPIO.output(pin_trigger[0], GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(pin_trigger[0], GPIO.LOW)


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
        while not GPIO.input(self.pin_trigger_int):
            pulse_start_time = time.time()
        while GPIO.input(self.pin_trigger_int):
            pulse_end_time = time.time()
        pulse_duration = pulse_end_time - pulse_start_time
        distance = round(pulse_duration * 17150, 2)
        defaultMaker.discord_report(json={"content":f"Distance: {distance} cm"})