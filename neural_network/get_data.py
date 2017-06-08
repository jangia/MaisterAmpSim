#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 26 17:15:24 2017

@author: jangia
"""
import datetime
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

real_model = Sequential()
real_model.add(Dense(units=NUM_SMAPLES, input_dim=NUM_SMAPLES, kernel_initializer='normal', activation='relu'))
real_model.add(Dense(units=NUM_SMAPLES, kernel_initializer='normal'))
real_model.compile(loss='mean_squared_error', optimizer='adam')

imag_model = Sequential()
imag_model.add(Dense(units=NUM_SMAPLES, input_dim=NUM_SMAPLES, kernel_initializer='normal', activation='relu'))
imag_model.add(Dense(units=NUM_SMAPLES, kernel_initializer='normal'))
imag_model.compile(loss='mean_squared_error', optimizer='adam')
cnt = 0
for amp in AMPS:
        
    print('Started at: ' + str(datetime.datetime.now()))
    
    # Get all FFTs
    fft_ref_all = pd.DataFrame(list(db.fft.find({'amp': str(AMPS[0])})))
    fft_all = pd.DataFrame(list(db.fft.find({'amp': str(AMPS[0])})))
    
    print('I have data from database at:' + str(datetime.datetime.now()) )
    
    dataset = fft_all.merge(fft_ref_all, how='inner', on=['amp', 'frequency'])
    
    f = dataset.iloc[:, 3].values
    
    print('Working for f={f} and amp={amp}'.format(f=str(f[cnt]), amp=amp))
    # Merge reference and mesured datasets
    cnt += 1
    # Set amplitude and input FFT as input data
    gain = np.float64(dataset.iloc[:, -3].values)[0]
    volume = np.float64(dataset.iloc[:, -1].values)[0]
    
    X3 = dataset.iloc[:, -4].values
    
    # Initialize real and imag array of FFT
    X_re = np.empty([56, 5000])
    
    X_im = np.empty([56, 5000])
    
    # Set output FFT
    Y = dataset.iloc[:, 2].values
    
    # Initialize real and imag array of output FFT
    Y_all_re = np.empty([56, 5000])
    Y_all_im = np.empty([56, 5000])
    
    # Set real and imag array of FFT
    
    for i in range(0, len(X3)):
        
        X_re[i][0] = gain
        X_re[i][1] = volume
        
        X_im[i][0] = gain
        X_im[i][1] = volume
            
        for j in range(0, NUM_SMAPLES):
            
            Y_all_re[i][j]= np.real(np.char.replace(Y[i][j], '', '').astype(np.complex128))
            Y_all_im[i][j] = np.imag(np.char.replace(Y[i][j], '', '').astype(np.complex128))
            
            if j < NUM_SMAPLES-2:
                X_re[i][j + 2] = np.real(np.char.replace(X3[i][j], '', '').astype(np.complex128))
                X_im[i][j + 2] = np.imag(np.char.replace(X3[i][j], '', '').astype(np.complex128))
    
    
    # Set real and imag array of output FFT
    #        for element in Y[0][0:NUM_SMAPLES]:
    #            Y_all_re = np.append(Y_all_re, np.real(np.char.replace(element, '', '').astype(np.complex128)))
    #            Y_all_im = np.append(Y_all_im, np.imag(np.char.replace(element, '', '').astype(np.complex128)))
    
    # Take only first 5000 components otherwise to much to compute
    #X_in_re = np.array([X_re[:NUM_SMAPLES]])
    #X_in_im = np.array([X_im[:NUM_SMAPLES]])
    #
    #Y_all_in_re = np.array([Y_all_re[:NUM_SMAPLES]])
    #Y_all_in_im = np.array([Y_all_im[:NUM_SMAPLES]])
    
    
    X_in_re = X_re
    X_in_im = X_im
    
    Y_all_in_re = Y_all_re
    Y_all_in_im = Y_all_im
    
    # Create real part of neural network
    
    real_model.fit(X_in_re, Y_all_in_re, batch_size=8, epochs=20)
    
    # Create imag part of neural network
    imag_model.fit(X_in_im, Y_all_in_im, batch_size=8, epochs=20)
    
    
    
    for h in range(0, len(X_in_re)):

        # Predicting the Test set results
        y_pred_real = real_model.predict(X_in_re[h:h+1])
        y_pred_imag = imag_model.predict(X_in_im[h:h+1])
        
        # Make FFT components from arrays
        out_pred = []
        out_meas = []
        
        for i in range(2, len(y_pred_real[0])):
            out_pred.append(np.complex(y_pred_real[0][i], y_pred_imag[0][i]))
            out_meas.append(np.complex(Y_all_in_re[h][i], Y_all_in_im[h][i]))
        
        pred = np.array(out_pred)
        
        #        for i in range(0, len(Y_all_in_re[0])):
        #            out_meas.append(np.complex(Y_all_in_re[0][i], Y_all_in_im[0][i]))
        
        meas = np.array(out_meas)
        
        plt.subplot(2, 1, 1)
        plt.semilogy(abs(meas[0:NUM_SMAPLES]),'r')
        plt.title('Measured Output VS Predicted Output')
        plt.ylabel('Amplitude')
        
        plt.subplot(2, 1, 2)
        plt.semilogy(abs(pred[2:NUM_SMAPLES]))
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Amplitude')
        
        filename = 'g{0}v{1}f{2}a{3}'.format(str(gain), str(volume), str(f[h]), str(amp)).replace('.', '_')
        plt.savefig('/home/jangia/Documents/Mag/MaisterAmpSim/neural_network/plots/{0}.png'.format(filename))
        
        plt.close()
    
    print('Finished at: ' + str(datetime.datetime.now()))
    
     