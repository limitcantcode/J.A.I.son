'''
Class implementing TTS generation using old-school speech synthesis.
This may require espeak for Linux. Voices available will differ between OS,
and available voices for your OS can be found using get_available_voices
'''

from .base_worker import BaseTTSGenWorker
import pyttsx3

class OldTTSWorker(BaseTTSGenWorker):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.engine = pyttsx3.init()
        self.engine.setProperty('voice', 'English (America)')
        self.engine.setProperty('gender', 'male')

    def tts(self, msg: str):
        self.engine.save_to_file(msg, self.output_filepath)
        self.engine.runAndWait()

    '''
    Get a list of available voices, names of which can be use to r
    eplace the 'voice' property in the __init__ function
    '''
    def get_available_voices(self):
        voices = self.engine.getProperty('voices')
        for ind in range(len(voices)):
            print(ind, voices[ind].id)