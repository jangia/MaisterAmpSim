# -*- coding: utf-8 -*-
from scipy.fftpack import fft as fft
from scipy.stats import signaltonoise as snr
from pymongo import MongoClient


def process_chunk(filename, frequency, chunk, data_len):
    
    
    # database entry
    db_entry = {
        "gain": filename[1],
        "volume": filename[3],
        "frequency": frequency,
        "amp": filename[5:-4].replace('_', '.'),
        "snr": str(snr(chunk)),
        "fft":[]
        }
    
    # calculate FFT
    chunk_fft = fft(chunk)
    
    # add FFTs to db_entry
    for i in range(0, data_len):
        db_entry['fft'].append(str(chunk_fft[i]))
      
    # database  
    client = MongoClient()
    db = client.amp
    
    db.fft.insert_one(db_entry)
    
    return 0

def fft_to_db(wave, samples, frequency, amplitude, data_len):
    
    # database entry
    db_entry = {
        "frequency": str(frequency) + '',
        "amp": str(amplitude) + '',
        "fft":[]
        }
    
    # calculate FFT
    chunk_fft = fft(wave[0: samples])
    
    # add FFTs to db_entry
    for i in range(0, data_len):
        db_entry['fft'].append(str(chunk_fft[i]))
      
    # database  
    client = MongoClient()
    db = client.amp
    
    db.fft_ref.insert_one(db_entry)
    
    return 0
    
    
        