import logging


class Invoker(object):
    def __init__(self):
        self.list_of_commands = []

    def _find_command_by_request(self, request):
        for command in self.list_of_commands:
            try:
                request_list = [word.lower() for word in request.split()]
                if all(word.lower() in request_list for word in command.voice_command.request_text.split()):
                    return command
            except (AttributeError, TypeError):
                pass

        raise CommandNotRecognized("command not recognized")

    def execute(self, command_request_text):
        """
        :param command_request_text: Request text, e.g.: "Turn on the light in the kitchen"
        """

        # Find appropriate command of ICommand interface that is associated with text request.
        command = self._find_command_by_request(command_request_text)
        logging.info("Executing '%s' command." % command.voice_command.name)
        command.execute()

    def set_command(self, command):
        self.list_of_commands.append(command)


class CommandNotRecognized(Exception):
    pass
