#! /usr/bin/env python2.7
#coding=utf-8

import logging
import pymongo
from gensim import corpora, models, similarities
import jieba
import json

class tfidf():
     """docstring for tf-idf"""
     def __init__(self):
        conn = pymongo.Connection("localhost",27017)
        self.db = conn.falcon
     def tf(self):
        tf_list = dict()
        while self.db.ptext1.find_one({"tf":{"$exists":False}}) is not None:
            weibo = self.db.ptext1.find_one({"tf":{"$exists":False}})
            print weibo
            count =0 
            text = weibo["text"]
            sid =  weibo["_id"]
            print sid
            seg_list = jieba.cut(text,cut_all=False)
            print "Default Mode:", "/ ".join(seg_list) #精确模式
            for word in seg_list:
                count += 1
                # print r.encode("utf-8")
                if tf_list.has_key(word):
                    tf_list[word] += 1
                else:
                    tf_list[word] = 1
            print '\n'
            # tf_list = json.dumps(tf_list)
            print tf_list
            result = self.db.ptext1.update({"_id":sid},{"$set":{"tf":0}},upsert=True)
            print result
            # print count
            topa = self.db.ptext1.find({"tf":1})

if __name__ == '__main__':
    ob = tfidf()
    ob.tf()

