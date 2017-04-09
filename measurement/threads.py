import threading

import scipy.io.wavfile
import sounddevice as sd
import time

from measurement.generators import Generators


class AudioInterfaceThread (threading.Thread):

    def __init__(self, thread_id, name, audio_device_manager, generator):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.audio_device_manager = audio_device_manager
        self.generator = generator

    def run(self):
        print("Starting " + self.name)
        if self.name == 'Thread-play':
            samples = self.generator.generate_sweep()

            self.audio_device_manager.play(samples)

        else:
            self.audio_device_manager.record()

        time.sleep(5)

        print("Exiting " + self.name)

