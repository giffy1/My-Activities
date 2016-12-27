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
# You should keep it in the format "speaker-data-<activity>-#.csv"
filename="activity-data-walking-1.csv" #"activity-data-walking-1.csv"

# TODO: Change the label to match the activity; it must be numeric
label = 2

data_dir = "data"

if not os.path.exists(data_dir):
    os.mkdir(data_dir)

labelled_data = []

def write_data(data, callback=None):
    """
    Writes the data point to the buffer.
    """
    t=data['t']
    values = data['values']
    global labelled_data
    labelled_instance = [t]
    labelled_instance.extend(values)
    labelled_instance.append(label)
    labelled_data.append(labelled_instance)

def save_data_to_disk():
    """
    Saves the data buffer to disk.
    """
    global labelled_data
    with open(os.path.join(data_dir, filename), "wb") as f:
        np.savetxt(f, labelled_data, delimiter=",")