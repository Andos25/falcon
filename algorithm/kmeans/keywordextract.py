#!/usr/bin/env python
#coding=utf-8

import sys
import pymongo

def get_inCollection():
    mongo = pymongo.Connection("localhost", 27017)["weibo"]
    return mongo["text"]

def get_outCollection():
    mongo = pymongo.Connection("localhost", 27017)["weibo"]
    return mongo["cluster"]

def run():
    inCollection = get_inCollection()#weibo.text
    outCollection = get_outCollection()#weibo.cluster
    file = open("/home/hadoop/kmeansdata/kmeansres2w.txt")#each line is a cluster,{}\tid@id@id@{}\n
    linelist = list()
    wordfre = dict()#all words in a cluster, key:word; value:word frequency
    keyword = list()
    clusterId = 1
    lines = file.readlines()
    for line in lines:
        keyword = []
        linelist = line.split('\t')[1].split('@')
        linelist.pop()
        print "linelist length:", len(linelist)
        for i in range(len(linelist)-1):#blogId in a cluster
            tf = inCollection.find_one({"_id":int(linelist[i])})["tf"]
            for j in range(len(tf)):
                if wordfre.has_key(tf.keys()[j]):
                    wordfre[tf.keys()[j]] += 1
                else:
                    wordfre[tf.keys()[j]] = 1
        tmp = sorted(wordfre, key=wordfre.get)
        print "tmp length:", len(tmp)
        if len(tmp) > 2:
        	keyword.append(tmp[len(tmp)-1])
        	keyword.append(tmp[len(tmp)-2])
        	keyword.append(tmp[len(tmp)-3])
        else:
        	keyword.append(tmp[len(tmp)-1])
        outCollection.save({"_id":clusterId, "blogsum":len(linelist), "blist":linelist, "keyword":keyword})
        clusterId += 1

if __name__ == '__main__':
    run()