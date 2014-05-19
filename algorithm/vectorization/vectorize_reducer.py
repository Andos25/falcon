#!/usr/bin/env python
#coding=utf-8

import pymongo
import sys
import json
import re

def get_incollection():
    mongo = pymongo.Connection("master", 27017)["weibo"]
    return mongo["idf"]

def get_outcollection():
    mongo = pymongo.Connection("master", 27017)["weibo"]
    return mongo["text"]

def get_file():
    return open("/home/hadoop/kmeansdata/vector913.txt", 'w')

def run():
    reload(sys)
    sys.setdefaultencoding('utf-8')
    res = dict()#针对一条微博blogId:{vector}
    f = get_file()
    print "get idf"
    inCollection = get_incollection()
    cIdf = {}
    for record in inCollection.find():
        cIdf[record['word']] = [record['id'], record['idf']]
    print "get text"
    # for line in sys.stdin:#针对一条微博的一个单词#blogId@word\ttf
    for line in sys.stdin:
        tf = line.strip().split('\t')[1]
        blogId = line.strip().split('\t')[0].split('@')[0]
        word = line.strip().split('\t')[0].split('@')[1].decode('utf-8')
        if re.search(r'\W', word):
            print "{0}\t{1}".format(blogId,word)
            if res.has_key(blogId):
                res[blogId][cIdf[word][0]] = float(tf) * float(cIdf[word][1])
            else:
                res[blogId] = {}
                res[blogId][cIdf[word][0]] = float(tf) * float(cIdf[word][1])
    print "write res"
    tmpOut = ""
    for i in range(len(res)):
        key = int(float(res.keys()[i]))
        value = res.values()[i]
        tmpOut = tmpOut + "{0}\t{1}\n".format(key, value)
        if i%2000 == 0:
            f.write(tmpOut)
            tmpOut = ""
    f.write(tmpOut)
    f.close()


if __name__ == '__main__':
    run()
