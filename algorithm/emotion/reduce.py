#!/usr/bin/python
#coding=utf-8

import pymongo
import sys
sys.path.append('./libsvm-3.1/python')
from svmutil import *
import json

def get_collection(name):
    conn = pymongo.Connection("localhost", 27017)
    return conn["weibo"][name]

def run():
    collection = get_collection("text")
    model = svm_load_model("model_file")
    for i in sys.stdin:
        _id, value = i.split("\t")
        value = json.loads(value)
        for key in value.keys():
            value[int(key)] = value.pop(key)
        if value == False:
            collection.update({"_id": int(_id)}, {"$set": {"em": 0}})
        else:
            result = svm_predict2(value, model)
            collection.update({"_id": int(_id)}, {"$set": {"em": result}})

if __name__ == '__main__':
    run()


