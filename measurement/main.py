import os
import wavio
from scipy import signal
import numpy as np
import sounddevice as sd


# set data
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REC_PATH = os.path.join(BASE_DIR, 'recordings')
AMPS = [0.1*1.25**i for i in range(0, 21)]
FS = 192000
F0 = 10
F1 = 300
T_END = 5
D_TYPE = 'float32'

# main
base_filename = input("Write file name: ")

if base_filename:

    # for every amplitude

    for amp in AMPS:

        print('Measuring on amplitude: {0}'.format(amp))

        # set file path
        filepath = os.path.join(REC_PATH, base_filename + str(amp).replace('.', '_') + '.wav')


        # set signal
        t = np.linspace(0, T_END, T_END*FS)
        samples = signal.chirp(t, f0=F0, f1=F1, t1=T_END).astype(np.float32)


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