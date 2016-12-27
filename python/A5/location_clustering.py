# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 15:34:11 2016

@author: cs390mb

Location Clustering : k-Means / Mean Shift

This Python script clusters location data using k-Means / Mean Shift.

"""

import socket
import sys
import json
import numpy as np
from sklearn.cluster import KMeans, MeanShift

def cluster(data, send_clusters, *args):
    """
    Clusters the given locations according to the algorithm specified.
    
    TODO: You should construct a N x 2 matrix of (latitude, longitude) pairs, 
    where N is the number of locations (= len(latitudes) = len(longitudes)).
    
    Then according to the algorithm parameter ("k_means" or "mean_shift"), 
    call the appropriate scikit-learn function. For k-means, k=args[0].
    
    Like classification algorithms, first create an instance of the clustering 
    algorithm object. Then the clustering is done using the fit() 
    function. The indexes of those points are then acquired using the 
    labels_ field.
        
    The Android application will receive the cluster indexes.
    
    """
    
    algorithm = data['algorithm']
    latitudes=data['latitudes']
    longitudes=data['longitudes']
    
    if algorithm == "k_means":
        k = data['k']
     
    data = {'indexes' : []} # change empty list to the list of indexes
    send_clusters("CLUSTER", data)
    
    # TODO : Create N x 2 matrix of lat-long values
    
    # TODO : Run the algorithm, then send the cluster indexes back to the phone
    
    return
    