#!/usr/bin/env python
#coding=utf-8

import pymongo
import sys
import json

def get_incollection():
    mongo = pymongo.Connection("192.168.40.161", 27017)["weibo"]
    return mongo["idf"]

def get_outcollection():
    mongo = pymongo.Connection("192.168.40.161", 27017)["weibo"]
    return mongo["text"]

def run():
    inCollection = get_incollection()#weibo.idf
    outCollection = get_outcollection()#weibo.text
    count = 0
    newline = list()
    res = dict()#针对一条微博blogId:[vector]
    for n in inCollection.find().sort('id', -1).limit(1):
        n = n['id']+1#向量长度
    for line in sys.stdin:#针对一条微博的一个单词
        newline = line.strip().split('\t') #blogId@word\ttf
        # print newline
        tf = newline[1]
        blogWord = newline[0].split('@')
        blogId = blogWord[0]
        word = blogWord[1]
        wordId = inCollection.find_one({"word": word})['id']#start from 0
        wordIdf = inCollection.find_one({"word": word})['idf']
        tfIdf = float(tf) * float(wordIdf)
        if res.has_key(blogId):#res[key]:blogId;res[value]:{wordId:word_tfidf;wordId:word_tfidf}
            res[blogId][wordId] = tfIdf
        else:
            # res[blogId] = [0 for i in range(n+1)]
            res[blogId] = {}
            res[blogId][wordId] = tfIdf
        # print "ok"
    # print "for finished,len(res)=", len(res)
    for i in range(len(res)):
        # print i
        # print int(float(res.keys()[i])), res.values()[i]
        key = int(float(res.keys()[i]))
        print key, res.values()[i]
        # value = json.dumps(res.values()[i])
        # outCollection.update({"_id": key}, {"$set": {"v": value}}, upsert = True)


if __name__ == '__main__':
    run()