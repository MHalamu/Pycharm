from Commands.voice_commands import VoiceCommandsContainer
from Invoker.invoker import CommandNotRecognized
import logging


class VoiceAssist(object):

    HELLO_PI_SIMILARS = ["hello pie", "hello pipe", "hello by",
                         "hello vine", "hello pine", "Hello hi"]
    NO_COMMAND = "no"

    def __init__(self, invoker, voice_recognizer):
        self.invoker = invoker
        self.voice_recognizer = voice_recognizer

    def _wait_for_hello(self):
        while True:
            logging.info("Waiting for 'Hello Pi...'")
            voice_text = self.voice_recognizer.listen_for_voice()
            if any((text in voice_text.lower() for text in self.HELLO_PI_SIMILARS)):
                VoiceCommandsContainer.GREETING.execute()
                return

    def _wait_for_voice_command(self):
        while True:
            logging.info("Waiting for voice command...")
            return self.voice_recognizer.listen_for_voice()

    def run(self):
        while True:
            #self._wait_for_hello()

            while True:
                # Request text, e.g.: "Turn on the light in the kitchen"
                #command_request_text = VoiceCommandsContainer.ASSIGN_RELAY.request_text
                command_request_text = self._wait_for_voice_command()

                if command_request_text == self.NO_COMMAND:
                    # Nothing else to do. Going back to waiting for "Hello Pi".
                    VoiceCommandsContainer.ALRIGHT_THANK_YOU.execute()
                    break

                try:
                    self.invoker.execute(command_request_text)
                except CommandNotRecognized:
                    VoiceCommandsContainer.CMD_NOT_RECOGNIZED.execute()
                    continue

                VoiceCommandsContainer.IS_ANYTHING_ELSE.execute()
