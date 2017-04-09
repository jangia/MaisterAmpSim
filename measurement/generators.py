import numpy as np
from scipy import signal


class Generators:

    def __init__(self, f0, f1, t_end, fs, volume):

        self.f0 = f0
        self.f1 = f1
        self.t_end = t_end
        self.fs = fs
        self.volume = volume

    def generate_sine_wave(self, f=440, duration=5, volume=0.5, fs=44100):
        """
        :param f: integer - frequency that you want to generate
        :param volume: float - between [0, 1]
        :param fs: integer - sampling frequency
        :return: samples: numpy array of sine wave
        """
        samples = volume*(np.sin(2 * np.pi * np.arange(fs * duration) * f / fs)).astype(np.float64)

        return samples

    def generate_sweep(self):

        t = np.linspace(0, self.t_end, self.fs*self.t_end)
        samples = self.volume*signal.chirp(t, f0=self.f0, f1=self.f1, t1=self.t_end).astype(np.float64)

        return samples
