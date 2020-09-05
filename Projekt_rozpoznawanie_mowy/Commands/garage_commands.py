from Commands.command_interface import ICommand
import time


class OpenGarageDoorCommand(ICommand):

    def __init__(self, gpio_controller, pin, voice_command):
        self.gpio_controller = gpio_controller
        self.gpio_controller.set_output_pin(pin)
        if not self.gpio_controller.pwm_pin:
            self.gpio_controller.set_pwm_pin(pin, 50)
        self.voice_command = voice_command

    def execute(self):
        self.gpio_controller.set_pwm_duty_cycle(self.gpio_controller.pwm_pin, 2)
        self.voice_command.execute()
        time.sleep(3)
        self.gpio_controller.set_pwm_duty_cycle(self.gpio_controller.pwm_pin, 0)


class CloseGarageDoorCommand(ICommand):

    def __init__(self, gpio_controller, pin, voice_command):
        self.gpio_controller = gpio_controller
        self.gpio_controller.set_output_pin(pin)
        if not self.gpio_controller.pwm_pin:
            self.gpio_controller.set_pwm_pin(pin, 50)
        self.pin = pin
        self.voice_command = voice_command

    def execute(self):
        self.gpio_controller.set_pwm_duty_cycle(self.gpio_controller.pwm_pin, 9)
        self.voice_command.execute()
        time.sleep(3)
        self.gpio_controller.set_pwm_duty_cycle(self.gpio_controller.pwm_pin, 0)
