import RPi.GPIO as GPIO


class HeaterController:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)

    def turn_on(self):
        GPIO.output(self.pin, 1)

    def turn_off(self):
        GPIO.output(self.pin, 0)

heater = HeaterController(6)
heater.turn_on()
