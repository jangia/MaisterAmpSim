# -*- coding: utf-8 -*-

import pandas
from pymongo import MongoClient

client = MongoClient()
db = client.amp

cursor = db.fft.find()

for document in cursor:
    print(test_load)