import threading

import sounddevice as sd
import numpy as np
import _thread
import scipy.io.wavfile

sd.default.samplerate = 192000
sd.default.channels = 2
# volume = 0.3     # range [0.0, 1.0]
fs = 192000       # sampling rate, Hz, must be integer
# duration = 50.0   # in seconds, may be float
# f = 440.0        # sine frequency, Hz, may be float
#
# # generate samples, note conversion to float32 array
# samples = (np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32)
# sd.play(samples)

#


def record(filename='test123.wav'):

    try:
        duration = 5.5  # seconds
        print(sd.query_devices(sd.default.device)['name'])
        myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=2, dtype='float64')

        sd.wait()

        scipy.io.wavfile.write(filename, fs, myrecording)
    except Exception as e:
        print("Error: unable to start recording: {0}".format(e))


def play():
    try:
        volume = 0.2  # range [0.0, 1.0]
        fs = 44100  # sampling rate, Hz, must be integer
        duration = 5.0  # in seconds, may be float
        f = 440.0

        samples = volume*(np.sin(2 * np.pi * np.arange(fs * duration) * f / fs)).astype(np.float32)
        sd.play(samples)

        # sd.wait()
    except Exception as e:
        print(e)
# Create new threads
# play()
# threading.Thread(target=record).start()
# threading.Thread(target=play).start()

volume = 0.2  # range [0.0, 1.0]
fs = 44100  # sampling rate, Hz, must be integer
duration = 5.0  # in seconds, may be float
f = 440.0

samples = volume*(np.sin(2 * np.pi * np.arange(fs * duration) * f / fs)).astype(np.float32)

myrecording = sd.playrec(samples)

sd.wait()

scipy.io.wavfile.write('test123.wav', fs, myrecording)

# Start new Threads
# thread1.start()
# thread2.start()
# thread1.join()
# thread2.join()
print("Exiting Main Thread")

# def record(filename):
#     import sounddevice as sd
#     try:
#         duration = 5.5  # seconds
#         print(sd.query_devices(sd.default.device)['name'])
#         myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=2, dtype='float64')
#
#         sd.wait()
#
#         scipy.io.wavfile.write(filename, fs, myrecording)
#     except Exception as e:
#         print("Error: unable to start recording: {0}".format(e))
#
#
# # Create two threads as follows
# try:
#     _thread.start_new_thread(record, ('test.wav',))
# except Exception as e:
#     print("Error: unable to start thread: {0}".format(e))
# filename = 'test.wav'
# try:
#     duration = 5.5  # seconds
#     myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=2, dtype='float64')
#
#     sd.wait()
#
#     scipy.io.wavfile.write(filename, fs, myrecording)
# except Exception as e:
#     print("Error: unable to start recording: {0}".format(e))