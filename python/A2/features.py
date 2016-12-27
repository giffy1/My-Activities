# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 13:08:49 2016

@author: cs390mb

Activity Recognition : Feature Extraction

This script provides methods for extracting various features that 
could be used for the activity recognition task. You are provided 
with the _compute_mean_features() method and must complete several 
others as part of the assignment.

"""

import numpy as np

def _compute_mean_features(window):
    """
    Computes the mean x, y and z acceleration over the given window. 
    Returns a length-3 vector [mean X, mean Y, mean Z].
    """
    return np.mean(window, axis=0)


def extract_features(window):
    """
    Here is where you will extract your features from the data over 
    the given window. We have given you an example of computing 
    the mean and appending it to the feature vector x.
    
    x can be of any size, as long as you are consistent when you 
    train and when you test your application (order must be 
    consistent too!). This shouldn't be a problem since you'll 
    be calling this same method.
    
    For example, if you decide to compute (in addition to the 3 mean 
    values) 3 variances, the mean magnitude, the variance of the magnitude 
    and the top 2 dominant frequencies of the Z-axis, then you will have 
    3 + 3 + 1 + 1 + 2 = 10 features. Then x will be a length-10 array.
    
    """
    
    # the magnitude can be computed easily over an entire window, 
    # using numpy functions. Remember magnitude = sqrt(X^2 + Y^2 + Z^2).
    # Notice the value of axis! If you leave out the axis, you will get 
    # a sum over ALL the values in the window instead, which is not the magnitude.
    magnitude = np.sqrt(np.sum(np.square(window), axis=1))
    
    x = []
    
    x = np.append(x, _compute_mean_features(window))
    
    return x