import numpy as np
from scipy import signal


def generate_sine_wave(f, volume=0.5, fs=44100, duration=5.0):
    """
    :param f: integer - frequency that you want to generate
    :param volume: float - between [0, 1]
    :param fs: integer - sampling frequency
    :return: samples: numpy array of sine wave
    """
    samples = volume*(np.sin(2 * np.pi * np.arange(fs * duration) * f / fs)).astype(np.float32)

    return samples


def generate_square_wave(f, volume=0.5, fs=44100, duration=5.0):
    """
    :param f: integer - frequency that you want to generate
    :param volume: float - between [0, 1]
    :param fs: integer - sampling frequency
    :return: samples: numpy array of sine wave
    """

    t = np.linspace(0, 1, 500, endpoint=False)
    samples = signal.square(2 * np.pi * 5 * t)
    # samples = volume*(np.square(2 * np.pi * np.arange(fs * duration) * f / fs)).astype(np.float32)

    return samples
