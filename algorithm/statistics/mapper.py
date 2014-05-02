#!/usr/bin/env python
#coding=utf-8

import sys
sys.path.append("../../")
sys.path.append("../../common/")
import jieba
import pymongo
import re

def get_collection():
    mongo = pymongo.Connection("localhost", 27017)["weibo"]
    return mongo["users"] 

def run():
    collection = get_collection()
    for i in collection.find():
        try:
            if i["gender"] == 'm':
                print "{0}\t{1}".format(i["province"]*100+i["city"], 0)
            elif i["gender"] == 'f':
                print "{0}\t{1}".format(i["province"]*100+i["city"], 1)
            else:
                print "{0}\t{1}".format(i["province"]*100+i["city"], 2)
        except:
            continue

if __name__ == '__main__':
    run()
