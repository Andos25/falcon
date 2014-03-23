#!/usr/bin/env python
#coding=utf-8

import sys
import math
sys.path.append("../../")
sys.path.append("../../common/")
from common.MongoConnection import MongoConnection

def get_collection():
    mongo = MongoConnection()
    collection = mongo.get_collection("weibo", "text")
    # cursor = collection.find()
    return collection

def run():
    collection = get_collection()
    filesum = float(collection.count())
    wordlist = dict()
    for line in sys.stdin:
        word, value = line.rstrip().split('\t', 1)
        if wordlist.has_key(word):
            wordlist[word] += 1
        else:
            wordlist[word] = 1
    for word in wordlist.keys():
        collection.save({"word": word, "idf": math.log(filesum/wordlist[word])})

if __name__ == '__main__':
    run()
