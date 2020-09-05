try:
    import RPi.GPIO as GPIO
except:
    from unittest.mock import Mock
    GPIO = Mock()

import logging


class GpioController(object):
    def __init__(self):
        GPIO.setwarnings(False)  # Ignore warning for now
        GPIO.setmode(GPIO.BOARD)  # Use physical pin numbering

    def set_output_pin(self, pin):
        GPIO.setup(pin, GPIO.OUT)

    def get_pwm_pin(self, pin, frequency):
        pwm_pin = GPIO.PWM(pin, frequency)
        pwm_pin.start(0)
        return pwm_pin

    def set_high(self, pin):
        logging.info("Turning on pin %s" % pin)

        GPIO.output(pin, GPIO.HIGH)

    def set_low(self, pin):
        logging.info("Turning off pin %s" % pin)
        GPIO.output(pin, GPIO.LOW)

    def set_pwm_duty_cycle(self, pwm_pin, duty_cycle):
        pwm_pin.ChangeDutyCycle(duty_cycle)
