import RPi.GPIO as GPIO




class BaseSensor:


    def __init__(self, mode, setup, pin: int):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.IN)    
        self.pin = pin


    def __exit__(self, exc_type, exc_value, traceback):
        GPIO.cleanup()