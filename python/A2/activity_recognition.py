# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 15:34:11 2016

@author: cs390mb

Activity Recognition : Prediction

This Python script receives live unlabelled accelerometer data through 
the server and uses your trained classifier to predict its activity label. 
The label is then sent back to the Android application via the server.

"""

import sys
import os
import threading
import numpy as np
import pickle
from features import extract_features

# Load the classifier (this was generated when you ran the training script):
A2_directory = os.path.dirname(os.path.abspath(__file__))
output_dir = 'training_output'
classifier_filename = 'classifier.pickle'

with open(os.path.join(A2_directory, output_dir, classifier_filename), 'rb') as f:
    classifier = pickle.load(f)
    
if classifier == None:
    raise Exception("Classifier is null; make sure you have trained it!")

def _predict(window, on_activity_detected):
    """
    Given a window of accelerometer data, predict the activity label. 
    Then use the onActivityDetected() method to notify the 
    Android must use the same feature extraction that you used to 
    train the model.
    """
    
    print("Buffer filled. Making prediction over window...")
    
    # TODO: Predict class label
    
    on_activity_detected("ACTIVITY_DETECTED", "WALKING")
    
    return

sensor_data = [] # sensor data buffer
window_size = 25 # ~1 sec assuming 25 Hz sampling rate
step_size = 25 # no overlap (same as window size)
index = 0 # to keep track of how many samples we have buffered so far

def buffer_and_predict(data, on_activity_detected):
    global index
    global sensor_data
    
    x = data['x']
    y = data['y']
    z = data['z']
    
    sensor_data.append((x,y,z)) # add to buffer
    index+=1 # increment
    # make sure we have exactly window_size data points :
    while len(sensor_data) > window_size:
        sensor_data.pop(0)

    # once the buffer is filled, make predictions:
    if (index >= step_size and len(sensor_data) == window_size):
        activity_recognition_thread = threading.Thread(target=_predict,  args=(np.asarray(sensor_data[:]),on_activity_detected))
        activity_recognition_thread.start()
        index = 0 # reset index