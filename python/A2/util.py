# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 11:00:51 2016

@author: cs390mb

Activity Recognition : Utility Functions

Includes various utility functions.

"""
 
def slidingWindow(sequence,winSize,step=1):
    """Returns a generator that will iterate through
    the defined chunks of input sequence.  Input sequence
    must be iterable.
    Thanks to https://scipher.wordpress.com/2010/12/02/simple-sliding-window-iterator-in-python/"""
 
    # Verify the inputs
    try: 
        it = iter(sequence)
    except TypeError:
        raise Exception("**ERROR** sequence must be iterable.")
    if not ((type(winSize) == type(0)) and (type(step) == type(0))):
        raise Exception("**ERROR** type(winSize) and type(step) must be int.")
    if step > winSize:
        raise Exception("**ERROR** step must not be larger than winSize.")
    if winSize > len(sequence):
        raise Exception("**ERROR** winSize must not be larger than sequence length.")
 
    # Pre-compute number of chunks to emit
    numOfChunks = ((len(sequence)-winSize)/step)+1
 
    # Do the work
    for i in range(0,numOfChunks*step,step):
        yield i, sequence[i:i+winSize]