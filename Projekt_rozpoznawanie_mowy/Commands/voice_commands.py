from Commands.command_interface import ICommand
from VoiceUtils.text_to_speech import TextToSpeech


class VoiceCommand(ICommand):
    def __init__(self, name, response_text, request_text=None):
        self.name = name
        self.request_text = request_text
        self.response_text = response_text

    def execute(self):
        TextToSpeech.play_recording(self.name)


class VoiceCommandsContainer(object):

    GREETING = VoiceCommand("greeting", "Hello, what can I do for you?")
    CMD_NOT_RECOGNIZED = VoiceCommand("cmd_not_recognized", "Sorry, I didn't get this. Try again.")
    IS_ANYTHING_ELSE = VoiceCommand("is_anything_else", "Can I do anything else for you?")
    TURN_ON_LIGHT_KITCHEN = VoiceCommand("Light_on_kitchen", "Turning on light in the kitchen.", "turn on light kitchen")
    TURN_OFF_LIGHT_KITCHEN = VoiceCommand("Light_off_kitchen", "Turning off light in the kitchen.", "turn off light kitchen")

    OPEN_GARAGE_DOOR = VoiceCommand("open_garage_door", "Opening the garage.", "open garage")
    CLOSE_GARAGE_DOOR = VoiceCommand("close_garage_door", "Closing the garage.", "close garage")

    TURN_ON_LIGHT_BEDROOM = VoiceCommand("Light_on_bedroom", "Turning on light in the bedroom.", "turn on light bedroom")
    TURN_OFF_LIGHT_BEDROOM = VoiceCommand("Light_off_bedroom", "Turning off light in the bedroom.", "turn off light bedroom")
    TURN_ON_LOCK_MAIN_DOOR = VoiceCommand("lock_main_door", "The main door has been locked", "lock main door")
    TURN_OFF_LOCK_MAIN_DOOR = VoiceCommand("unlock_main_door", "The main door has been unlocked", "unlock main door")
    ASSIGN_RELAY = VoiceCommand("assign_relay", "Please provide number of the relay you want to define", "define relay")
    NOT_A_NUMBER = VoiceCommand("not_a_number", "This is not a number. Please try again.")
    ALRIGHT_THANK_YOU = VoiceCommand("alright_thank_you", "Ok, have a nice day.")
