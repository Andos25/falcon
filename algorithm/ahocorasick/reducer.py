#!/usr/bin/env python
#coding=utf-8

import pymongo
import sys
import json

def get_collection(name):
    conn = pymongo.Connection("localhost", 27017)
    return conn["weibo"][name]

def run():
    collection = get_collection("text")
    for item in sys.stdin:
        try:
            key, value = item.split("\t", 1)
        except:
            continue
        value = json.loads(value)
        ac = set(value["ac"])
        cutwords = set(value["cutwords"])
        value = list(ac & cutwords)
        if(len(value) != 0):
            collection.update({"_id": int(key)}, {"$set": {"kwords": value}})

if __name__ == '__main__':
    run()