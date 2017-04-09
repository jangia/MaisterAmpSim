import scipy.io.wavfile
import sounddevice as sd

from measurement.generators import Generators


class AudioDeviceManager:

    def __init__(self, filepath, fs=44100, duration=10, channels=2, dtype='float64'):
        self.filepath = filepath
        self.fs = fs
        self.duration = duration
        self.channels = channels
        self.dtype = dtype

    def record(self):
        """
        Function for recording on your recording device
        writes your recording to file
        :return: void
        """

        try:
            print(sd.query_devices(sd.default.device)['name'])

            print('Starting recording')

            myrecording = sd.rec(
                int(self.duration * self.fs),
                samplerate=self.fs,
                channels=self.channels,
                dtype=self.dtype)
            print('Recording ...')
            sd.wait()

            print('Writing to file: {0}'.format(self.filepath))
            scipy.io.wavfile.write(self.filepath, self.fs, myrecording)

        except Exception as e:
            print("Error: unable to record".format(e))

    def play(self, samples=''):

        try:
            generator = Generators(f0=0, f1=5000, t_end=5, fs=44100, volume=0.2)

            samples = generator.generate_sweep()
            sd.play(samples)

            sd.wait()
        except Exception as e:
            print('Error trying to play: {0}'.format(e))