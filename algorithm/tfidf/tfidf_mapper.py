#!/usr/bin/env python
#coding=utf-8

import sys
sys.path.append("../../")
sys.path.append("../../common/")
import jieba
import pymongo

def get_collection():
    mongo = pymongo.Connection("127.0.0.1", 27017)["weibo"]
    return mongo["text"] 

def run():
    stopword = [i.rstrip() for i in open('/home/hadoop/falcon/algorithm/tfidf/stopword')]
    collection = get_collection()
    cursor = collection.find()
    for item in cursor:
        try:
            words = jieba.cut(item["text"], cut_all=False)
        except:
            continue
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
        print item["_id"]
        collection.update({"_id":item["_id"]}, {"$set": {"tf": wordlist}})

if __name__ == '__main__':
    run()
