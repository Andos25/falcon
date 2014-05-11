#!/usr/bin/env python
# coding=utf-8

import pymongo
import sys
sys.path.append('./libsvm-3.1/python')
from svmutil import *

def get_collection(name):
    conn = pymongo.Connection("localhost", 27017)
    return conn["weibo"][name]

def run():
    collection = get_collection("text")
    idfcollection = get_collection("idf")
    model = svm_load_model("model_file")
    count = 0
    for text in collection.find():
        tflist = text["tf"]
        print count
        count += 1
        if tflist == {}:
            text["em"] = 0
            collection.save(text)
            continue
        value = dict()
        for i in tflist.keys():
            idf = idfcollection.find_one({"word": i})
            value[idf["id"]] = idf["idf"] * tflist[i] * 100
        result = svm_predict2(value, model)
        text["em"] = result
        collection.save(text)

if __name__ == '__main__':
    run()