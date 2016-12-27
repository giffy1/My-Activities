# -*- coding: utf-8 -*-
"""
Created on Fri Nov  4 13:07:01 2016

@author: cs390mb

Data Collection : Data Processing

This script is intended to provide an introduction to 
Python and to make sure that you can successfully 
bidirectional communication with your Android application.

"""

def compute_average(data, send_notification):
    """
    Compute the average for each axis of accelerometer data every 100 samples. 
    This method is called for each sample and the data is stored in "data".
    You can access it as follows:
    
        data['x'], data['y'], data['z'] or data['t'] 
    
    for the x-, y-, z-values and time respectively.
        
    When the average is computed, send it back over the server by first wrapping 
    the averages in a Python dictionary:
    
        json = {"average_X" : x_average, "average_Y": y_average, "average_Z": z_average}
        
    Then call
    
        send_notification("AVERAGE_ACCELERATION", json)
        
    You can compute the average by maintaining sums and a counter. Since these 
    variables must be accessible with each call, you should make them global. 
    Global variables are defined outside the scope of the method. Then inside 
    the method, they can only be accessed if you first specify it as global, e.g. 

        global sum_X
    
    """    
    
    # TODO: Compute average acceleration
    
    # replace dummy values with the values you compute:
    json = {"average_X" : 0., "average_Y" : 0., "average_Z": 9.8} 
    send_notification("AVERAGE_ACCELERATION", json)
    
    return