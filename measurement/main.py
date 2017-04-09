import os

import sys

from measurement.audio_device_manager import AudioDeviceManager
from measurement.generators import Generators
from measurement.threads import AudioInterfaceThread

import sounddevice as sd

args = sys.argv
base_filename = args[1]
amp = args[2]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

rec_path = os.path.join(BASE_DIR, 'recordings')

th_id = 0

filepath = os.path.join(rec_path, base_filename + str(amp).replace('.', '_') + '.wav')

print('Your saved file will have name: {0}'.format(filepath))

print('Measuring on amplitude: {0}'.format(amp))
audio_device_manager = AudioDeviceManager(filepath, 44100, 5)

generator = Generators(f0=0, f1=5000, t_end=5, fs=44100, volume=amp)
rec_thread = AudioInterfaceThread(th_id, 'Thread-record', audio_device_manager, generator)

play_thread = AudioInterfaceThread(th_id, 'Thread-play', audio_device_manager, generator)


# threading.Thread(target=audio_device_manager.play).start()
# threading.Thread(target=audio_device_manager.record).start()

play_thread.start()
rec_thread.start()

play_thread.join()
rec_thread.join()

print("Exiting Main Thread")

