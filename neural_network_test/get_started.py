#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 25 09:00:16 2017

@author: jangia
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack
import scipy.stats
import scipy.io.wavfile
import scipy.signal
from pymongo import MongoClient

# read all records and cut them
# make fft
# save fft to db
# create neural network

# input signal
AMPS = [0.90**i for i in range(0, 26)]
FS = 96000
F0 = 10
F1 = 2000
T_END = 1
D_TYPE = 'float32'

samples = np.zeros(shape=(1))

for i in range(-30, 27):
            f = 440 * (2 ** (1 / 12)) ** i
            t = np.arange(FS * T_END)
            sine_wave = np.sin(2 * np.pi * f * t / FS)

            samples = np.concatenate([samples, sine_wave])
# 
#
#N = 30000
#
#f = 440 * (2 ** (1 / 12)) ** 0
#t = np.arange(FS * T_END)
#sine_wave = np.sin(2 * np.pi * f * t / FS)
#
#yf = scipy.fftpack.fft(sine_wave)
#
#f = np.linspace (FS,len(sine_wave), endpoint=False)
#
#abs_fft = np.abs(yf)
#d = int(round(len(abs_fft) / 20))
#
#plt.semilogy(abs_fft[:d-1],'r')
#
##plt.plot(sine_wave[0:1000])
#plt.show()

#print(scipy.stats.signaltonoise(sine_wave))

# read file
REC_PATH = '/home/jangia/Documents/Mag/MaisterAmpSim/recordings/g4v4_0_9.wav'

rate, data = scipy.io.wavfile.read(REC_PATH)

#plt.plot(scipy.signal.detrend(data[30000:60000], type='constant'),'r')
#plt.show()

#norm_audio = [(ele / 2 ** rate) * 2 for ele in data[1000:10000]]
#print(scipy.stats.signaltonoise(scipy.signal.detrend(data[30000:60000])))

#no_offset = scipy.signal.detrend(data[30000:60000])


#norm_audio = [(ele / 2 ** rate) * 2 for ele in data]
mono = [item[0] for item in data[10000:96000]]
#mono = data[400000:440000]
#norm_audio = [(ele / 2 ** rate) * 2 for ele in mono]

dataf = scipy.fftpack.fft(mono)

#f = np.linspace (FS,len(norm_audio), endpoint=False)

abs_fft = abs(dataf)
d = int(round(len(abs_fft)/100))


plt.subplot(2, 1, 1)
plt.semilogy(abs(dataf[:d-1]),'r')
plt.title('A tale of 2 subplots')
plt.ylabel('Damped oscillation')

plt.subplot(2, 1, 2)
plt.plot(mono)
plt.xlabel('time (s)')
plt.ylabel('Undamped')

plt.show()

print(scipy.stats.signaltonoise(mono))
print(str(dataf[0]))
            

#[b,a] = scipy.signal.butter(10, 50/(FS/2), 'highpass');
#neki = scipy.signal.filtfilt(b,a,data[30000:60000], padlen=0);

