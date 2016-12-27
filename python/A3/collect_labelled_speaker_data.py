# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 15:34:11 2016

@author: cs390mb

Speaker Identification : Data Collection

This Python script receives incoming labelled audio data through 
the server and saves it in .csv format to disk.

"""

import numpy as np
import os

# TODO: Change the filename of the output file.
# You should keep it in the format "speaker-data-<speaker>-#.csv"
filename="speaker-data-none-1.csv" # "speaker-data-KanyeWest-1.csv"

# TODO: Change the label to match the speaker; it must be numeric
label = 0

data_dir = "data"

if not os.path.exists(data_dir):
    os.mkdir(data_dir)

labelled_data = []

def write_data(data, callback=None):
    """
    Writes the data point to the buffer.
    """
    t=data['t']
    audio_buffer = data['values']
    global labelled_data
    labelled_instance = [t]
    labelled_instance.extend(audio_buffer)
    labelled_instance.append(label)
    labelled_data.append(labelled_instance)

def save_data_to_disk():
    """
    Saves the data buffer to disk.
    """
    global labelled_data
    with open(os.path.join(data_dir, filename), "wb") as f:
        np.savetxt(f, labelled_data, delimiter=",")