import os
import wavio
from scipy import signal
import numpy as np
import sounddevice as sd


# set data
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REC_PATH = os.path.join(BASE_DIR, 'recordings')
AMPS = [0.90**i for i in range(0, 26)]
FS = 96000
F0 = 10
F1 = 2000
T_END = 1
D_TYPE = 'float32'

sd.default.device = 'Babyface Pro'

# main
base_filename = input("Write file name: ")

if base_filename:

    # for every amplitude

    for amp in AMPS:

        print('Measuring on amplitude: {0}'.format(amp))

        # set file path
        filepath = os.path.join(REC_PATH, base_filename + str(amp).replace('.', '_') + '.wav')

        samples = np.zeros(shape=(1))

        # set signal
        for i in range(-30, 27):
            f = 440 * (2 ** (1 / 12)) ** i
            t = np.arange(FS * T_END)
            sine_wave = np.sin(2 * np.pi * f * t / FS)

            samples = np.concatenate([samples, sine_wave])


        # recording
        print('Recording ...')
        my_recording = sd.playrec(samples, FS, channels=2, dtype=D_TYPE)
        sd.wait()
        print('Finish recording ...')


        # write to file
        print('Writing to file: {0}'.format(filepath))
        wavio.write(filepath, my_recording, FS, sampwidth=1)

        print('Script finished')

else:
    print('File name to short')