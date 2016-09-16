# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 15:34:11 2016

Assignment A0 : Data Collection

@author: cs390mb & Group 5 - Colin Stern

This Python script receives incoming data through the server and 
passes it to the process() method on a separate thread. Your job 
is to complete the process() method.

Refer to the assignment details at goo.gl/U3zzE0. For a beginner's 
tutorial on coding in Python, see goo.gl/aZNg0q.

"""

import socket
import sys
import json
import threading
import numpy as np

# TODO: Replace the string with your user ID
user_id = "75.6d.a4.38.38.e7.2d.96.76.a9"

sumX = 0
sumY = 0
sumZ = 0
counter = 0

def process(timestamp, values):


    """
    Process incoming accelerometer data.
    
    You will implement this method in assignment A0. All you need to do 
    is average the incoming values along each axis and print the averages 
    to the console.
    
    You can do this by maintaining a sum variable for each axis and a counter.
    
    This method is running on its own thread, therefore if you use any global 
    variables, you must declare them outside of the method and then re-declare 
    them global within the scope of the method. For instance, if you wish to 
    modify the same sumX in all calls of this method, use
    
        global sumX
        
    This should be done within the method, but the sumX must already be defined 
    and initialized outside the method scope.
    
    To increment the counter, you can NOT use counter++. It's invalid Python 
    syntax. But you can use
        counter += 1 
    or 
        counter = counter + 1
    
    Use the print method to print to the console. You can use the + operator 
    to concatenate strings, or you can use the .format string method. Here 
    is a simple example:
    
        print("My name is {} and I am the TA for {}".format("Sean", "390MB"))

    Each set of brackets represents a replaceable value.
    
    """
    print("Received data")

    global sumX
    global sumY
    global sumZ
    global counter


    sumX += values[0]
    sumY += values[1]
    sumZ += values[2]
    counter += 1
 
    if counter >= 100:
        print(str(sumX/counter) + " " + str(sumY/counter) + " " +  str(sumZ/counter))   
        sumX = 0
        sumY = 0
        sumZ = 0
        counter = 0
       
#################   Server Connection Code  ####################

'''
    This socket is used to send data back through the data collection server.
    It is used to complete the authentication. It may also be used to send 
    data or notifications back to the phone, but we will not be using that 
    functionality in this assignment.
'''
send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
send_socket.connect(("none.cs.umass.edu", 9999))

'''
    This socket is used to receive data from the data collection server
'''
receive_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
receive_socket.connect(("none.cs.umass.edu", 8888))
# ensures that after 1 second, a keyboard interrupt will close
receive_socket.settimeout(1.0)

msg_request_id = "ID"
msg_authenticate = "ID,{}\n"
msg_acknowledge_id = "ACK"

def authenticate(sock):
    """
    Authenticates the user by performing a handshake with the data collection server.
    
    If it fails, it will raise an appropriate exception.
    """
    message = sock.recv(256).strip()
    if (message == msg_request_id):
        print("Received authentication request from the server. Sending authentication credentials...")
        sys.stdout.flush()
    else:
        print("Authentication failed!")
        raise Exception("Expected message {} from server, received {}".format(msg_request_id, message))
    sock.send(msg_authenticate.format(user_id))

    try:
        message = sock.recv(256).strip()
    except:
        print("Authentication failed!")
        raise Exception("Wait timed out. Failed to receive authentication response from server.")
        
    if (message.startswith(msg_acknowledge_id)):
        ack_id = message.split(",")[1]
    else:
        print("Authentication failed!")
        raise Exception("Expected message with prefix '{}' from server, received {}".format(msg_acknowledge_id, message))
    
    if (ack_id == user_id):
        print("Authentication successful.")
        sys.stdout.flush()
    else:
        print("Authentication failed!")
        raise Exception("Authentication failed : Expected user ID '{}' from server, received '{}'".format(user_id, ack_id))


try:
    print("Authenticating user for receiving data...")
    sys.stdout.flush()
    authenticate(receive_socket)
    
    print("Authenticating user for sending data...")
    sys.stdout.flush()
    authenticate(send_socket)
    
    print("Successfully connected to the server! Waiting for incoming data...")
    sys.stdout.flush()
        
    previous_json = ''
        
    while True:
        try:
            message = receive_socket.recv(1024).strip()
            json_strings = message.split("\n")
            json_strings[0] = previous_json + json_strings[0]
            for json_string in json_strings:
                try:
                    data = json.loads(json_string)
                except:
                    previous_json = json_string
                    continue
                previous_json = '' # reset if all were successful
                sensor_type = data['sensor_type']
                if (sensor_type == u"SENSOR_ACCEL"):
                    t=data['data']['t']
                    x=data['data']['x']
                    y=data['data']['y']
                    z=data['data']['z']
                    
                    processThread = threading.Thread(target=process, args=(t,[x,y,z]))
                    processThread.start()
                
            sys.stdout.flush()
        except KeyboardInterrupt: 
            # occurs when the user presses Ctrl-C
            print("User Interrupt. Quitting...")
            break
        except Exception as e:
            # ignore exceptions, such as parsing the json
            # if a connection timeout occurs, also ignore and try again. Use Ctrl-C to stop
            # but make sure the error is displayed so we know what's going on
            if (e.message != "timed out"):  # ignore timeout exceptions completely       
                print(e)
            pass
except KeyboardInterrupt: 
    # occurs when the user presses Ctrl-C
    print("User Interrupt. Quitting...")
finally:
    print >>sys.stderr, 'closing socket for receiving data'
    receive_socket.shutdown(socket.SHUT_RDWR)
    receive_socket.close()
    
    print >>sys.stderr, 'closing socket for sending data'
    send_socket.shutdown(socket.SHUT_RDWR)
    send_socket.close()