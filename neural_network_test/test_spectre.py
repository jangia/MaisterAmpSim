#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 18 19:04:47 2017

@author: jangia
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack

# Number of samplepoints
N = 30000
# sample spacing
T = 1.0 / 800.0
x = np.linspace(0.0, N*T, N)
y = np.sin(440.0 * 2.0*np.pi*x)
yf = scipy.fftpack.fft(y)
xf = np.linspace(0.0, 1.0/(2.0*T), N/2)

fig, ax = plt.subplots()
ax.plot(xf, 2.0/N * np.abs(yf[:N//2]))
plt.show()

#np.savetxt('outfile.txt', yf.view(float).reshape(-1, 2))
#array = np.loadtxt('outfile.txt').view(complex).reshape(-1)

# test = yf.view(float).reshape(-1, 2)

entry = {
        "gain": "2",
        "volume": "4",
        "fft":{}
        }

for i in range(0, len(yf)):
    entry['fft'][str(i)] = str(yf[i])
    
test = np.char.replace(entry['fft']['0'], '', '').astype(np.complex128)

np.append(test, test)
    
from pymongo import MongoClient

client = MongoClient()
db = client.amp

result = db.fft.insert_one(entry)

cursor = db.fft.find()

for document in cursor:
    test_load = document['fft']['0'].view(complex).reshape(-1)
    print(test_load)
    
# db.fft.delete_many({"borough": "Manhattan"})