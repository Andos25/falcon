#!/usr/bin/python
#coding=utf-8

import pymongo
import json

def get_collection(name):
    conn = pymongo.Connection("localhost", 27017)
    return conn["weibo"][name]

def run():
    collection = get_collection("text")
    idfcollection = get_collection("idf")
    for text in collection.find().limit(10):
        tflist = text["tf"]
        if tflist == {}:
            print str(text["_id"]) + "\t" + json.dumps(False)
        value = dict()
        for i in tflist.keys():
            idf = idfcollection.find_one({"word": i})
            value[idf["id"]] = idf["idf"] * tflist[i] * 100
        print str(text["_id"]) + "\t" + json.dumps(value)

if __name__ == '__main__':
    run()