from Commands.command_interface import ICommand


class LockCommand(ICommand):

    def __init__(self, gpio_controller, pin, voice_command):
        self.gpio_controller = gpio_controller
        self.pin = pin
        self.voice_command = voice_command

    def execute(self):
        self.gpio_controller.on(self.pin)
        self.voice_command.execute()


class UnlockCommand(ICommand):

    def __init__(self, gpio_controller, pin, voice_command):
        self.gpio_controller = gpio_controller
        self.pin = pin
        self.voice_command = voice_command

    def execute(self):
        self.gpio_controller.off(self.pin)
        self.voice_command.execute()
