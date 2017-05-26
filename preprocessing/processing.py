#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 25 12:25:31 2017

@author: jangia
"""
import os
import threading
from process_record.edit_record import cut_record
from process_record.process_chunk import process_chunk


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath('processing.py')))

REC_PATH = os.path.join(BASE_DIR, 'recordings')

files = [f for f in os.listdir(REC_PATH) if os.path.isfile(os.path.join(REC_PATH, f))]


for file in files:
    
    # chunk file
    audio_chunks = cut_record(os.path.join(REC_PATH, file), 96000, 80000, 57, 10000)
    
    for frq, chunk in audio_chunks.items():
        # run proccessing
        
        t = threading.Thread(target=process_chunk, args = (file,frq, chunk))
        t.daemon = True
        t.start()
    


    