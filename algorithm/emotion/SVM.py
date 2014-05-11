#!/usr/bin/env python
#coding=utf-8

import sys
sys.path.append('./libsvm-3.1/python')
from svmutil import *

def train( filename, data_type = False):
    if data_type == False:
        y, x = svm_read_problem(filename)
    else:
        y, x = svm_read_problem(format_data(filename, data_type))
    model = svm_train(y, x, '-c 40 -t 2 -h 0')
    return model

def save_model( model, model_file):
    svm_save_model(model_file, model)

def load_model( model_file):
    model = svm_load_model(model_file)
    return model

def predict1( model_file, datafile):
    y, x = svm_read_problem(datafile)
    try:
        model = svm_load_model(model_file)
    except:
        model = model_file
    pred_labels,accuracy,pred_values = svm_predict1(y, x, model)
    return pred_labels, accuracy, pred_values

if __name__ == '__main__':
    model = train("tfidf")
    save_model(model, "model_file")
    model_file = load_model("model_file")
    predict1(model_file, "tfidf")