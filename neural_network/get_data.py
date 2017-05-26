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
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

client = MongoClient()
db = client.amp

fft_ref = pd.DataFrame(list(db.fft_ref.find({'frequency': '440.0', 'amp': '1.0'})))
fft = pd.DataFrame(list(db.fft.find({'amp': '1.0', 'frequency': '440.0'})))

dataset = fft.merge(fft_ref, how='inner', on=['amp', 'frequency'])

X1 = dataset.iloc[:, 1].values
X2 = dataset.iloc[:, 3].values
X3 = dataset.iloc[:, -1].values

X_fft = []

for element in X3[0]:
    X_fft = np.append(X_fft, np.char.replace(element, '', '').astype(np.complex128))

X = np.concatenate((X1, X2, X_fft))
Y = dataset.iloc[:, 2].values



# define base model
def baseline_model():
	# create model
	model = Sequential()
	model.add(Dense(3, input_dim=3, kernel_initializer='normal', activation='relu'))
	model.add(Dense(1, kernel_initializer='normal'))
	# Compile model
	model.compile(loss='mean_squared_error', optimizer='adam')
	return model
