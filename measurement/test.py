import os
import wavio
from scipy import signal
import numpy as np
import sounddevice as sd

def butter_highpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = signal.butter(order, normal_cutoff, btype='high', analog=False)
    return b, a

def butter_highpass_filter(data, cutoff, fs, order=5):
    b, a = butter_highpass(cutoff, fs, order=order)
    y = signal.filtfilt(b, a, data)
    return y

# set data
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REC_PATH = os.path.join(BASE_DIR, 'recordings')
AMPS = [0.87**i for i in range(0, 21)]
FS = 48000
F0 = 10
F1 = 2000
T_END = 1
D_TYPE = 'float32'
amp = 1
sd.default.device = 'Babyface Pro'
# print(sd.query_devices())
# main
base_filename = 'test'

if base_filename:

    # for every amplitude
    print('Measuring on amplitude: {0}'.format(amp))

    # set file path
    filepath = os.path.join(REC_PATH, base_filename + str(amp).replace('.', '_') + '.wav')

    samples = np.zeros(shape=(1))
    # set signal
    # for i in range(-57, 27):
    for i in range(-1, 1):
        f = 440 * (2**(1/12))**i
        t = np.arange(FS*T_END)
        sine_wave = np.sin(2 * np.pi * f * t / FS)

        samples = np.concatenate([samples,sine_wave])

    # recording
    print('Recording ...')
    my_recording = sd.playrec(samples, FS, input_mapping=[2], dtype=D_TYPE)
    sd.wait()
    print('Finish recording ...')

    # write to file
    print('Writing to file: {0}'.format(filepath))
    # filtered_recording = butter_highpass_filter(my_recording, 10, FS, 5)
    wavio.write(filepath, my_recording, FS, sampwidth=1)

    print('Script finished')

else:
    print('File name to short')