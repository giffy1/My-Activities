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
from ...client import Client

# TODO: Change this to match your activities
activities = ["walking", "running"]

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
        
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: %s <activity> <index, default=1>" % sys.argv[0])
    else:
        if len(sys.argv) == 2:
            index=1
        else:
            index = sys.argv[2]
        activity = sys.argv[1]
        label = activities.index(activity)
        data_dir = "data"
        filename="activity-data-" + str(activity) + "-" + str(index) + ".csv"

        if not os.path.exists(data_dir):
            os.mkdir(data_dir)

        c = Client("") # TODO: Pass in user ID
        # To collect activity data, uncomment just these next two lines:
        c.map_data_to_function("SENSOR_ACCEL", collect_labelled_activity_data.write_data)
        c.set_disconnect_callback(collect_labelled_activity_data.save_data_to_disk)
        
        # connect to the server to begin:
        c.connect()