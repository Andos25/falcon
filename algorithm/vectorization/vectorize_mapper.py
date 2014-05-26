#!/usr/bin/env python
#coding=utf-8

import pymongo
import sys


def get_collection():
    mongo = pymongo.Connection("master", 27017)["weibo"]
    return mongo["text"]

def run():
    reload(sys)
    sys.setdefaultencoding('utf-8')
    collection = get_collection()
    tf = dict()
    for blogText in collection.find({"tf":{"$exists":True}, "_id":{"$lt":400000}}):
        if len(blogText['tf'])>0:#过滤一些类型不合法的tf
            blogId = blogText['_id']
            tf = blogText['tf']
            for i in range(len(tf)):
                key = str(blogId) + '@' + tf.keys()[i] #tf.keys()[i] => word
                value = tf.values()[i]
                print "{0}\t{1}".format(key, value)#key:blogId@word; value:tf


if __name__ == '__main__':
    run()
