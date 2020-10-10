from command_interface import ICommand


class LightOnCommand(ICommand):

    CMD_NAME = "LightOn"

    def __init__(self, light):
        self.light = light

    def execute(self):
        self.light.set_high()

    def unexecute(self):
        self.light.set_low()


class LightOffCommand(ICommand):

    CMD_NAME = "LightOff"

    def __init__(self, light):
        self.light = light

    def execute(self):
        self.light.set_low()

    def unexecute(self):
        self.light.set_high()
