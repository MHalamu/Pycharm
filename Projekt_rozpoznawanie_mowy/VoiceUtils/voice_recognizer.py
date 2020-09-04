import speech_recognition as sr
import logging


class VoiceRecognizer(object):

    PHRASE_TIME_LIMIT = 3

    def __init__(self, mic_index):
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone(device_index=mic_index, sample_rate=48000)
        with self.mic as source:
            self.recognizer.adjust_for_ambient_noise(source)

    def listen_for_voice(self):
        while True:
            try:
                with self.mic as source:
                    logging.info("Waiting for voice input...")
                    audio = self.recognizer.listen(source, 1, self.PHRASE_TIME_LIMIT)
                recognized_speech = self.recognizer.recognize_google(audio)
                logging.info("Recognized speech: %s" % recognized_speech)
                return recognized_speech

            except sr.UnknownValueError:
                logging.warning("I Cannot understand your command.")
            except sr.WaitTimeoutError:
                pass
