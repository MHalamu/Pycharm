from unittest.mock import Mock
import logging
GPIO = Mock()


class GpioController(object):
    def __init__(self):
        GPIO.setwarnings(False)  # Ignore warning for now
        GPIO.setmode(GPIO.BOARD)  # Use physical pin numbering

    def on(self, pin): # to trzebia zmienic na low/high
        logging.info("Turning on pin %s" % pin)
        GPIO.setup(pin, GPIO.OUT) # To trzeba by gdzies upchnac wczesniej zeby nie bylo ustawiane za kazdym razem
        GPIO.output(pin, GPIO.HIGH)  # Turn on

    def off(self, pin):
        logging.info("Turning off pin %s" % pin)
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)  # Turn on




# Trzeba gdzie (moze tu) dodac sterowanie pwm dla servo.