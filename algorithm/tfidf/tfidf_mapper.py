#!/usr/bin/env python
#coding=utf-8

import sys
sys.path.append("../../")
sys.path.append("../../common/")
import jieba
from common.MongoConnection import MongoConnection

def get_collection():
    mongo = MongoConnection()
    collection = mongo.get_collection("weibo", "text")
    return collection

def run():
    stopword = [i.rstrip() for i in open('stopword')]
    collection = get_collection()
    cursor = collection.find().limit(5)
    for item in cursor:
        words = jieba.cut(item["text"], cut_all=False)
        wordlist = dict()
        count = 0
        for word in words:
            word = word.encode('utf-8')
            if word in stopword:
                continue
            count += 1
            if wordlist.has_key(word):
                wordlist[word] += 1
            else:
                wordlist[word] = 1
        count = float(count)
        for word in wordlist.keys():
            wordlist[word] = wordlist[word]/count
            print "{0}\t{1}".format(word, 1)
        collection.update({"_id":item["_id"]}, {"$set": {"tf": wordlist}})

if __name__ == '__main__':
    run()
