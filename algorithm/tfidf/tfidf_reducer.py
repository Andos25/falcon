#!/usr/bin/env python
#coding=utf-8

import sys
import math
sys.path.append("../../")
sys.path.append("../../common/")
import pymongo

def get_collection(collectionname):
    mongo = pymongo.Connection("192.168.40.161", 27017)["weibo"]
    # cursor = collection.find()
    return mongo[collectionname]

def run():
    collection = get_collection("idf")
    filesum = float(get_collection("text").count())
    print filesum
    wordlist = dict()
    for line in sys.stdin:
        try:
            word, value = line.rstrip().split('\t', 1)
        except:
            continue
        if wordlist.has_key(word):
            wordlist[word] += 1
        else:
            wordlist[word] = 1
    for word in wordlist.keys():
        collection.save({"word": word, "idf": math.log(filesum/wordlist[word])})

if __name__ == '__main__':
    run()
