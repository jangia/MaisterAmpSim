#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 26 17:15:24 2017

@author: jangia
"""

import pandas as pd
import numpy as np
from pymongo import MongoClient
from keras.models import Sequential
from keras.layers import Dense
import matplotlib.pyplot as plt

NUM_SMAPLES = 5000
# create DB connection
client = MongoClient()
db = client.amp

AMPS = [0.90**i for i in range(0, 26)]

for amp in AMPS:
    
    for i in range(-30, 27):
        
        f = 440 * (2 ** (1 / 12)) ** i
    
        # Get all FFTs
        fft_ref_all = pd.DataFrame(list(db.fft_ref.find({'amp': str(amp), 'frequency': str(f)})))
        fft_all = pd.DataFrame(list(db.fft.find({'amp': str(amp), 'frequency': str(f)})))
        
        print('I have data')
        
        dataset = fft_all.merge(fft_ref_all, how='inner', on=['amp', 'frequency'])
        
        real_model = Sequential()
        real_model.add(Dense(units=NUM_SMAPLES, input_dim=NUM_SMAPLES, kernel_initializer='normal', activation='relu'))
        real_model.add(Dense(units=NUM_SMAPLES, kernel_initializer='normal'))
        real_model.compile(loss='mean_squared_error', optimizer='adam')
        
        imag_model = Sequential()
        imag_model.add(Dense(units=NUM_SMAPLES, input_dim=NUM_SMAPLES, kernel_initializer='normal', activation='relu'))
        imag_model.add(Dense(units=NUM_SMAPLES, kernel_initializer='normal'))
        imag_model.compile(loss='mean_squared_error', optimizer='adam')
        
        # Merge reference and mesured datasets
        
        # Set amplitude and input FFT as input data
        gain = np.float64(dataset.iloc[:, 4].values)
        volume = np.float64(dataset.iloc[:, 6].values)
        
        X3 = dataset.iloc[:, -1].values
        
        
        # Initialize real and imag array of FFT
        X_re = []
        X_re.append(gain)
        X_re.append(volume)
        
        X_im = []
        X_im.append(gain)
        X_im.append(volume)
        
        # Set real and imag array of FFT
        for element in X3[0][0:NUM_SMAPLES-2]:
            X_re = np.append(X_re, np.real(np.char.replace(element, '', '').astype(np.complex128)))
            X_im = np.append(X_im, np.imag(np.char.replace(element, '', '').astype(np.complex128)))
        
        # Set output FFT
        Y = dataset.iloc[:, 2].values
        
        # Initialize real and imag array of output FFT
        Y_all_re = []
        Y_all_im = []
        
        # Set real and imag array of output FFT
        for element in Y[0][0:NUM_SMAPLES]:
            Y_all_re = np.append(Y_all_re, np.real(np.char.replace(element, '', '').astype(np.complex128)))
            Y_all_im = np.append(Y_all_im, np.imag(np.char.replace(element, '', '').astype(np.complex128)))
        
        # Take only first 5000 components otherwise to much to compute
        #X_in_re = np.array([X_re[:NUM_SMAPLES]])
        #X_in_im = np.array([X_im[:NUM_SMAPLES]])
        #
        #Y_all_in_re = np.array([Y_all_re[:NUM_SMAPLES]])
        #Y_all_in_im = np.array([Y_all_im[:NUM_SMAPLES]])
        
        X_in_re = np.array([X_re])
        X_in_im = np.array([X_im])
        
        Y_all_in_re = np.array([Y_all_re])
        Y_all_in_im = np.array([Y_all_im])
        
        # Create real part of neural network
        
        real_model.fit(X_in_re, Y_all_in_re, batch_size=100)
        
        # Create imag part of neural network
        imag_model.fit(X_in_im, Y_all_in_im, batch_size=100)
        
        
        # Predicting the Test set results
        y_pred_real = real_model.predict(X_in_re)
        y_pred_imag = imag_model.predict(X_in_im)
        
        # Make FFT components from arrays
        out_pred = []
        
        for i in range(2, len(y_pred_real[0])):
            out_pred.append(np.complex(y_pred_real[0][i], y_pred_imag[0][i]))
        
        pred = np.array(out_pred)
        
        out_meas = []
        
        for i in range(0, len(Y_all_in_re[0])):
            out_meas.append(np.complex(Y_all_in_re[0][i], Y_all_in_im[0][i]))
        
        meas = np.array(out_meas)
        
        plt.subplot(2, 1, 1)
        plt.semilogy(abs(meas[0:NUM_SMAPLES]),'r')
        plt.title('Input VS Output')
        plt.ylabel('Amplitude')
        
        plt.subplot(2, 1, 2)
        plt.plot(abs(pred[2:NUM_SMAPLES]))
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Amplitude')
        
        #filename = 'g{0}v{1}f{2}a{3}'.format(str(gain), str(volume), dataset.iloc[:, 3].values, dataset[:, 1].values)
        #plt.savefig('/home/jangia/Documents/Mag/MaisterAmpSim/neural_network/plots/{0}.png'.format(filename))
    
 