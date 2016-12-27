# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 15:34:11 2016

@author: cs390mb

Speaker Identification : Prediction

This Python script receives incoming unlabelled audio data through 
the server and uses your trained classifier to predict the speaker. 
The label is then sent back to the Android application via the server.

"""

import numpy as np
import pickle
from features import FeatureExtractor
import os

# Load the classifier:
A3_directory = os.path.dirname(os.path.abspath(__file__))
output_dir = 'training_output'
classifier_filename = 'classifier.pickle'

with open(os.path.join(A3_directory, output_dir, classifier_filename), 'rb') as f:
    classifier = pickle.load(f)
    
if classifier == None:
    raise Exception("Classifier is null; make sure you have trained it!")
    
feature_extractor = FeatureExtractor(debug=False)

# replace dummy values with speakers being identified:
speakers = ["Donald Trump", "Hillary Clinton", "Kanye West"]

def predict(window, on_speaker_detected, *args):
    """
    Given a window of audio data, predict the speaker. 
    Then use the onSpeakerDetected() method to notify the 
    Android application. You must use the same feature 
    extraction method that you used to train the model.
    """
    
    print("Buffer filled. Making prediction over window...")
    
    # TODO: Predict class label
    
    on_speaker_detected("SPEAKER_DETECTED", speakers[0]) # replace dummy value
    
    return