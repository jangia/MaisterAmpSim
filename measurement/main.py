import os
import time
import sounddevice as sd

from measurement.audio_device_manager import AudioDeviceManager
from measurement.threads import AudioInterfaceThread
from measurement.generators import Generators

# init
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

rec_path = os.path.join(BASE_DIR, 'recordings')

amps = [0.1*1.25**i for i in range(0, 21)]

# main loop
while 1:
    base_filename = input("Write file name: ")
    if base_filename:

        # for every amplitude
        th_id = 0

        for amp in amps:

            filepath = os.path.join(rec_path, base_filename + str(amp).replace('.', '_') + '.wav')

            print('Your saved file will have name: {0}'.format(filepath))

            print('Measuring on amplitude: {0}'.format(amp))
            audio_device_manager = AudioDeviceManager(filepath, 44100, 5)

            generator = Generators(f0=0, f1=5000, t_end=10, fs=44100, volume=amp)
            rec_thread = AudioInterfaceThread(th_id, 'Thread-record', audio_device_manager, generator)
            th_id += 1
            play_thread = AudioInterfaceThread(th_id, 'Thread-play', audio_device_manager, generator)
            th_id += 1

            play_thread.start()
            rec_thread.start()
            play_thread.join()
            rec_thread.join()

            # time.sleep(5 + 1)

            print("Exiting Main Thread")

