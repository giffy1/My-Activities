# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 15:34:11 2016

@author: cs390mb

Step Detection

This Python script receives incoming accelerometer data through the 
server, detects step events and sends them back to the server for 
visualization/notifications.

"""

# You may want to use numerical Python for quick and easy calculations, 
# e.g. np.mean(A). It is not required for this assignment, but future 
# assignments will require numpy so make sure you have it installed:
#       pip install numpy
import numpy as np

def detect_steps(data, on_step_detected, *args):
    """
    Accelerometer-based step detection algorithm.
    
    Implement your step detection algorithm. This may be functionally 
    equivalent to your Java step detection algorithm if you like. 
    Remember to use the global keyword if you would like to access global 
    variables such as counters or buffers. When a step has been detected, 
    call the onStepDetected method, passing in the timestamp:
    
        onStepDetected("STEP_DETECTED", timestamp)       
    
    """
    
    timestamp = data['t']
    x = data['x']
    y = data['y']
    z = data['z']
    
    # TODO: Step detection algorithm
    
    # TODO: call on_step_detected only when you detect a step:
    on_step_detected("STEP_DETECTED", {"timestamp" : timestamp})  
    
    return