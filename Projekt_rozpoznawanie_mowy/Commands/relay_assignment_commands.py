from Commands.command_interface import ICommand
from Commands.voice_commands import VoiceCommand, VoiceCommandsContainer
from Commands.relay_commands import EnableRelayCommand
from Controllers.pins_assignment import RELAY_MAP


class AssignRelayCommand(ICommand):

    def __init__(self, gpio_controller, voice_command, text_to_speech, voice_recognizer, invoker):
        self.gpio_controller = gpio_controller
        self.voice_command = voice_command
        self.text_to_speech = text_to_speech
        self.voice_recognizer = voice_recognizer
        self.invoker = invoker
        self.relay_number = None
        self.relay_name = None

    def _assign_relay_number(self):
        self.voice_command.execute()  
        try:
            self.relay_number = int(self.voice_recognizer.listen_for_voice())
        except ValueError:
            raise VoiceCommandsContainer.NOT_A_NUMBER.execute()
        
        assignment_command = VoiceCommand(
            "assign_relay_%s" % self.relay_number,
            "You are now assigning relay number %s" % self.relay_number)
        self.text_to_speech.add_recording(assignment_command)
        assignment_command.execute()

    def _assing_name_of_the_relay(self):
        assignment_command = VoiceCommand(
            "assign_name_for_relay_%s" % self.relay_number,
            "Please provide a name for command assigned to relay %s" % self.relay_number)
        self.text_to_speech.add_recording(assignment_command)
        assignment_command.execute()

        self.relay_name = self.voice_recognizer.listen_for_voice()

        relay_name_cmd = VoiceCommand(
            "relay_%s_name_replay" % self.relay_number,
            "Relay number %s is now assigned as %s" % (self.relay_number, self.relay_name))
        self.text_to_speech.add_recording(relay_name_cmd)
        relay_name_cmd.execute()

    def _create_on_off_commands(self):
        turn_on_relay_voice_command = VoiceCommand(
            "enable_relay_%s" % self.relay_number,
            "Turning on %s" % self.relay_name,
            "turn on %s" % self.relay_name)
        self.text_to_speech.add_recording(turn_on_relay_voice_command)

        turn_off_relay_voice_command = VoiceCommand(
            "disable_relay_%s" % self.relay_number,
            "Turning off %s" % self.relay_name,
            "turn off %s" % self.relay_name)
        self.text_to_speech.add_recording(turn_off_relay_voice_command)

        self.invoker.set_command(EnableRelayCommand(
            gpio_controller=self.gpio_controller, pin=RELAY_MAP[int(self.relay_number)],
            voice_command=turn_on_relay_voice_command))
        self.invoker.set_command(EnableRelayCommand(
            gpio_controller=self.gpio_controller, pin=RELAY_MAP[int(self.relay_number)],
            voice_command=turn_off_relay_voice_command))

    def execute(self):
        self._assign_relay_number()
        self._assing_name_of_the_relay()
        self._create_on_off_commands()
