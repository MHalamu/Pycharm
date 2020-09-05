from Commands.command_interface import ICommand


class LockCommand(ICommand):

    def __init__(self, gpio_controller, pin, voice_command):
        self.gpio_controller = gpio_controller
        self.gpio_controller.set_output_pin(pin)
        self.pin = pin
        self.voice_command = voice_command

    def execute(self):
        self.gpio_controller.set_high(self.pin)
        self.voice_command.execute()


class UnlockCommand(ICommand):

    def __init__(self, gpio_controller, pin, voice_command):
        self.gpio_controller = gpio_controller
        self.gpio_controller.set_output_pin(pin)
        self.pin = pin
        self.voice_command = voice_command

    def execute(self):
        self.gpio_controller.set_low(self.pin)
        self.voice_command.execute()
