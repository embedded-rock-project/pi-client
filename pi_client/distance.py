import RPi.GPIO as GPIO
import time
from http_reqs import defaultMaker
import asyncio


class DistanceSensor:

    # initialization. Does not inherit from BaseSensor due to different setup.
    # split input/output into tuple.
    def __init__(self, mode, pin_trigger, pin_echo, loop=None):
        self.enabled = False
        self.currently_detecting = False
        self.sensor_event = None
        self.pin_trigger_int = pin_trigger[0]
        self.pin_echo_int = pin_echo[0]
        GPIO.setmode(mode)
        GPIO.setup(pin_trigger[0], pin_trigger[1]) 
        GPIO.setup(pin_echo[0], pin_echo[1])
        self.loop = loop if loop else asyncio.get_event_loop()

    # do nothing on enter. Disabled by default.
    def __enter__(self):
        pass

    # cleanup on exit of class. 
    def __exit__(self, exc_type, exc_value, traceback):
        self.disable_sensor()
        GPIO.cleanup()

    # check if sensor is already disabled. Avoids calls on NoneTypes.
    def disable_sensor(self):
        if self.enabled:
            self.enabled = False
            self.sensor_event.cancel()

    # check if sensor is already enabled. Avoids multiple calls to check_distance.
    def enable_sensor(self):
        if not self.enabled:
            self.enabled = True
            self.sensor_event = self.loop.run_in_executor(None, self.check_distance)

    # check distance from sensor.
    def check_distance(self):
        while self.enabled:

            # turn on laser.
            GPIO.output(self.pin_trigger_int, True)
            
            # sleep for a brief moment.
            time.sleep(0.00001)

            #turn off sensor.
            GPIO.output(self.pin_trigger_int, False)
            
            # measure when pulse of laser returns back.
            while GPIO.input(self.pin_echo_int) == 0:
                pulse_start_time = time.time()

            # measure when pulse of laser finishes.
            while GPIO.input(self.pin_echo_int) == 1:
                pulse_end_time = time.time()
                
            # subtract time.
            pulse_duration = pulse_end_time - pulse_start_time
            
            #formula based on the hardware specs of the wave has a max range of 2 meters
            distance = round(pulse_duration * 17150, 2)

            # only do callback if distance is less than 100 (someone intercepted beam)
            if (distance <= 100):
                if (not self.currently_detecting):
                    result = ("distance", "report", f"Disturbance detected! Distance from sensor: {distance} cm")
                    defaultMaker.ws_server_report(*result)
                    self.currently_detecting = True
                    
            # do other callback to reset checkmark on page.
            else:
                if (self.currently_detecting):
                    result = ("distance", "report", "Disturbance not detected.")
                    defaultMaker.ws_server_report(*result)
                    self.currently_detecting = False
            time.sleep(1)
