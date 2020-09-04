import os
from gtts import gTTS


class TextToSpeech(object):

    RECORDINGS_PATH = "Recordings/"

    def add_recording(self, command):
        if not os.path.exists(self.RECORDINGS_PATH + command.name + ".mp3"):
            text_to_speech_obj = gTTS(command.response_text)
            text_to_speech_obj.save(self.RECORDINGS_PATH + command.name + ".mp3")

    @staticmethod
    def play_recording(voice_cmd_name):
        os.system("mpg321 -q Recordings/%s.mp3" % voice_cmd_name)
