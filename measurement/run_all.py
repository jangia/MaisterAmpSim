import os
import threading
import time
import sounddevice as sd
from measurement.audio_device_manager import *

from measurement.audio_device_manager import AudioDeviceManager
from measurement.threads import AudioInterfaceThread
from measurement.generators import Generators

# init

amps = [0.1*1.25**i for i in range(0, 21)]

# main loop
while 1:
    base_filename = input("Write file name: ")
    if base_filename:

        # for every amplitude

        for amp in amps:

            os.system("/home/jangia/Documents/VirtualEnv/amp/bin/python3.5 main.py " + str(base_filename) + ' ' + str(amp))

