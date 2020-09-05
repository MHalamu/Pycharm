import os
from gtts import gTTS


class TextToSpeech(object):

    RECORDINGS_PATH = "/Recordings/"

    def add_recording(self, command):
        current_path = os.getcwd()
        if not os.path.exists(current_path + self.RECORDINGS_PATH + command.name + ".mp3"):
            text_to_speech_obj = gTTS(command.response_text)
            text_to_speech_obj.save(current_path + self.RECORDINGS_PATH + command.name + ".mp3")

    @staticmethod
    def play_recording(voice_cmd_name):
        import socket
        if socket.gethostname() == 'MacBook-Pro-Michal.local':
            os.system("mpg321 -q Recordings/%s.mp3" % voice_cmd_name)
        else:
            os.system("sudo mpg321 -q Recordings/%s.mp3" % voice_cmd_name)

