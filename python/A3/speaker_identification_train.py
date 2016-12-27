# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 16:02:58 2016

@author: cs390mb

Speaker Identification : Training a Classifier

This script trains a classifier for identifying speaker from audio data. 
The script loads all labelled speaker audio data files in the specified directory. 
It extracts features from the raw data and trains and evaluates a classifier 
to identify the speaker.

"""

import os
import sys
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from features import extract_features
from sklearn import cross_validation
from sklearn.metrics import confusion_matrix
import pickle


# %%---------------------------------------------------------------------------
#
#		                 Load Data From Disk
#
# -----------------------------------------------------------------------------

data_dir = 'data' # directory where the data files are stored

output_dir = 'training_output' # directory where the classifier(s) are stored

if not os.path.exists(output_dir):
    os.mkdir(output_dir)

# the filenames should be in the form 'speaker-data-subject-1.csv', e.g. 'speaker-data-Erik-1.csv'. If they 
# are not, that's OK but the progress output will look nonsensical

# the set of classes, i.e. speakers. Modify this to suit your needs:
class_names = ["Donald Trump", "Hillary Clinton", "Kanye West"]

data = np.zeros((0,8002)) #8002 = 1 (timestamp) + 8000 (for 8kHz audio data) + 1 (label)

for filename in os.listdir(data_dir):
    if filename.endswith(".csv") and filename.startswith("speaker-data"):
        filename_components = filename.split("-") # split by the '-' character
        speaker = filename_components[2]
        print("Loading data for {}.".format(speaker))
        if speaker not in class_names:
            class_names.append(speaker)
        speaker_label = class_names.index(speaker)
        sys.stdout.flush()
        data_file = os.path.join(data_dir, filename)
        data_for_current_speaker = np.genfromtxt(data_file, delimiter=',')
        print("Loaded {} raw labelled audio data samples.".format(len(data_for_current_speaker)))
        sys.stdout.flush()
        data = np.append(data, data_for_current_speaker, axis=0)

print("Found data for {} speakers : {}".format(len(class_names), ", ".join(class_names)))

# %%---------------------------------------------------------------------------
#
#		                Extract Features & Labels
#
# -----------------------------------------------------------------------------

# TODO : Modify this to match the feature extraction code. It is set to 3 because the starter code returns 3 dummy values.
n_features = 3

print("Extracting features and labels for {} audio windows...".format(data.shape[0]))
sys.stdout.flush()

X = np.zeros((0,n_features))
y = np.zeros(0,)

for i,window_with_timestamp_and_label in enumerate(data):
    window = window_with_timestamp_and_label[1:-1] # remove timestamp and label
    label = data[i,-1]
    x = extract_features(window) 
    if (len(x) != X.shape[1]):
        print("Received feature vector of length {}. Expected feature vector of length {}.".format(len(x), X.shape[1]))
    X = np.append(X, np.reshape(x, (1,-1)), axis=0)
    y = np.append(y, label)
    
print("Finished feature extraction over {} windows".format(len(X)))
print("Unique labels found: {}".format(set(y)))
sys.stdout.flush()


# %%---------------------------------------------------------------------------
#
#		                Train & Evaluate Classifier
#
# -----------------------------------------------------------------------------

n = len(y)
n_classes = len(class_names)

print("\n")
print("---------------------- Decision Tree -------------------------")

#trees = [] # various decision tree classifiers 
#trees.append(DecisionTreeClassifier(criterion="entropy", max_depth=3))
#
#for tree_index, tree in enumerate(trees):
#
#    total_accuracy = 0.0
#    total_precision = [0.0, 0.0, 0.0, 0.0]
#    total_recall = [0.0, 0.0, 0.0, 0.0]
#    
#    cv = cross_validation.KFold(n, n_folds=10, shuffle=True, random_state=None)
#    for i, (train_indexes, test_indexes) in enumerate(cv):
#        X_train = X[train_indexes, :]
#        y_train = y[train_indexes]
#        X_test = X[test_indexes, :]
#        y_test = y[test_indexes]
#        tree = DecisionTreeClassifier(criterion="entropy", max_depth=3)
#        print("Fold {} : Training decision tree classifier over {} points...".format(i, len(y_train)))
#        sys.stdout.flush()
#        tree.fit(X_train, y_train)
#        print("Evaluating classifier over {} points...".format(len(y_test)))
#        
#        # predict the labels on the test data
#        y_pred = tree.predict(X_test)
#    
#        # show the comparison between the predicted and ground-truth labels
#        conf = confusion_matrix(y_test, y_pred, labels=[0,1,2,3])
#        
#        accuracy = np.sum(np.diag(conf)) / float(np.sum(conf))
#        precision = np.nan_to_num(np.diag(conf) / np.sum(conf, axis=1).astype(float))
#        recall = np.nan_to_num(np.diag(conf) / np.sum(conf, axis=0).astype(float))
#        
#        total_accuracy += accuracy
#        total_precision += precision
#        total_recall += recall
#        
#        print("The accuracy is {}".format(accuracy))  
#        print("The precision is {}".format(precision))    
#        print("The recall is {}".format(recall))
#        
#        print("\n")
#        sys.stdout.flush()
#        
#    print("The average accuracy is {}".format(total_accuracy/10.0))  
#    print("The average precision is {}".format(total_precision/10.0))    
#    print("The average recall is {}".format(total_recall/10.0))  
#    
#    print("Training decision tree classifier on entire dataset...")
#    tree.fit(X, y)
##    print("Saving decision tree visualization to disk...")
##    export_graphviz(tree, out_file='tree{}.dot'.format(tree_index), feature_names = feature_names)
#
#print("\n")
#print("---------------------- Random Forest Classifier -------------------------")
#total_accuracy = 0.0
#total_precision = [0.0, 0.0, 0.0, 0.0]
#total_recall = [0.0, 0.0, 0.0, 0.0]
#for i, (train_indexes, test_indexes) in enumerate(cv):
#    X_train = X[train_indexes, :]
#    y_train = y[train_indexes]
#    X_test = X[test_indexes, :]
#    y_test = y[test_indexes]
#    print("Fold {} : Training SVM classifier over {} points...".format(i, len(y_train)))
#    sys.stdout.flush()
#    C = 1.0  # SVM regularization parameter
#    clf = RandomForestClassifier(n_estimators=100)
#    clf.fit(X_train, y_train)
#    
#    print("Evaluating classifier over {} points...".format(len(y_test)))
#    # predict the labels on the test data
#    y_pred = clf.predict(X_test)
#
#    # show the comparison between the predicted and ground-truth labels
#    conf = confusion_matrix(y_test, y_pred, labels=[0,1,2,3])
#    
#    accuracy = np.sum(np.diag(conf)) / float(np.sum(conf))
#    precision = np.nan_to_num(np.diag(conf) / np.sum(conf, axis=1).astype(float))
#    recall = np.nan_to_num(np.diag(conf) / np.sum(conf, axis=0).astype(float))
#    
#    total_accuracy += accuracy
#    total_precision += precision
#    total_recall += recall
#    
#    print("The accuracy is {}".format(accuracy))  
#    print("The precision is {}".format(precision))    
#    print("The recall is {}".format(recall))
#    
#    print("\n")
#    sys.stdout.flush()
#    
#print("The average accuracy is {}".format(total_accuracy/10.0))  
#print("The average precision is {}".format(total_precision/10.0))    
#print("The average recall is {}".format(total_recall/10.0))  

# when ready, set this to the best model you found, trained on all the data:
print("Training RF classifier on entire dataset...")
best_classifier = RandomForestClassifier(n_estimators=100)
best_classifier.fit(X,y) 
classifier_filename='classifier.pickle'
print("Saving best classifier to {}...".format(os.path.join(output_dir, classifier_filename)))
with open(os.path.join(output_dir, classifier_filename), 'wb') as f: # 'wb' stands for 'write bytes'
    pickle.dump(best_classifier, f)