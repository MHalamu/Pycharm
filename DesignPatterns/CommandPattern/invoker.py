class Invoker(object):
    def __init__(self,
                 light_on_command,
                 light_off_command):
        self.light_on_command = light_on_command
        self.light_off_command = light_off_command

    def set_command(self):
        pass

    def on_button(self):
        self.light_on_command.execute()

    def off_button(self):
        self.light_off_command.execute()


class InvokerGeneral(object):
    def __init__(self):
        self.command_to_button_map = {}

    def execute(self, command_name):
        self.command_to_button_map[command_name].execute()

    def set_command(self, command_name, command):
        self.command_to_button_map[command_name] = command


