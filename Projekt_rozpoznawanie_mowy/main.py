import logging
from Commands.voice_commands import VoiceCommandsContainer
from Commands.light_commands import LightOffCommand, LightOnCommand
from Commands.lock_commands import LockCommand, UnlockCommand
from Commands.relay_assignment_commands import AssignRelayCommand

from VoiceUtils.text_to_speech import TextToSpeech
from VoiceUtils.voice_recognizer import VoiceRecognizer
from Controllers.gpio_controller import GpioController
from Invoker.invoker import Invoker
from VoiceUtils.voice_assist import VoiceAssist
from Controllers.pins_assignment import KITCHEN_LIGHT_PIN, BEDROOM_LIGHT_PIN, MAIN_DOOR_LOCK_PIN


logging.basicConfig(level=logging.INFO)


def _initialize_text_to_speech():
    logging.info('Initializing text_to_speech module...')
    text_to_speech = TextToSpeech()
    for voice_command in [VoiceCommandsContainer.GREETING, VoiceCommandsContainer.CMD_NOT_RECOGNIZED,
                          VoiceCommandsContainer.IS_ANYTHING_ELSE, VoiceCommandsContainer.TURN_ON_LIGHT_KITCHEN,
                          VoiceCommandsContainer.TURN_OFF_LIGHT_KITCHEN, VoiceCommandsContainer.TURN_ON_LOCK_MAIN_DOOR,
                          VoiceCommandsContainer.TURN_OFF_LOCK_MAIN_DOOR, VoiceCommandsContainer.ASSIGN_RELAY,
                          VoiceCommandsContainer.ALRIGHT_THANK_YOU]:
        text_to_speech.add_recording(voice_command)

    return text_to_speech


def _initialize_voice_recognizer():
    logging.info('Initializing voice recognizer...')
    voice_recognizer = VoiceRecognizer(mic_index=0)
    return voice_recognizer


def _initialize_commands_module(text_to_speech, voice_recognizer):
    logging.info('Initializing commands module...')
    invoker = Invoker()
    gpio_controller = GpioController()

    # Light On/Off in the kitchen
    invoker.set_command(LightOnCommand(
        gpio_controller=gpio_controller, pin=KITCHEN_LIGHT_PIN,
        voice_command=VoiceCommandsContainer.TURN_ON_LIGHT_KITCHEN))

    invoker.set_command(LightOffCommand(
        gpio_controller=gpio_controller, pin=KITCHEN_LIGHT_PIN,
        voice_command=VoiceCommandsContainer.TURN_OFF_LIGHT_KITCHEN))

    # Light On/Off in the bedroom
    invoker.set_command(LightOnCommand(
        gpio_controller=gpio_controller, pin=BEDROOM_LIGHT_PIN,
        voice_command=VoiceCommandsContainer.TURN_ON_LIGHT_KITCHEN))

    invoker.set_command(LightOffCommand(
        gpio_controller=gpio_controller, pin=BEDROOM_LIGHT_PIN,
        voice_command=VoiceCommandsContainer.TURN_OFF_LIGHT_KITCHEN))

    # Enable/Disable lock in the main door
    invoker.set_command(LockCommand(
        gpio_controller=gpio_controller, pin=MAIN_DOOR_LOCK_PIN,
        voice_command=VoiceCommandsContainer.TURN_ON_LOCK_MAIN_DOOR))

    invoker.set_command(UnlockCommand(
        gpio_controller=gpio_controller, pin=MAIN_DOOR_LOCK_PIN,
        voice_command=VoiceCommandsContainer.TURN_OFF_LOCK_MAIN_DOOR))

    # Assigning relays
    invoker.set_command(AssignRelayCommand(
        gpio_controller=gpio_controller,
        voice_command=VoiceCommandsContainer.ASSIGN_RELAY,
        text_to_speech=text_to_speech,
        voice_recognizer=voice_recognizer,
        invoker=invoker))

    return invoker


def main():
    voice_recognizer = _initialize_voice_recognizer()
    text_to_speech = _initialize_text_to_speech()
    invoker = _initialize_commands_module(text_to_speech, voice_recognizer)

    voice_assist = VoiceAssist(invoker, voice_recognizer)
    voice_assist.run()


if __name__ == '__main__':
    main()





