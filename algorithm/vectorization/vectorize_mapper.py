#!//usr/bin/env python
#coding=utf-8

import pymongo
import sys


def get_collection():
    mongo = pymongo.Connection("localhost", 27017)["weibo"]
    return mongo["text"]

def run():
    reload(sys)
    sys.setdefaultencoding('utf-8')
    collection = get_collection()
    tf = dict()
    for blogText in collection.find({"tf": {"$exists": True}}):
        if str(type(blogText['tf'])) == "<type 'dict'>":#过滤一些类型不合法的tf
            blogId = blogText['_id']
            tf = blogText['tf']
            for i in range(len(tf)):
                key = str(blogId) + '@' + tf.keys()[i] #tf.keys()[i] => word
                value = tf.values()[i]
                print '%s\t%s' % (key, value)#key:blogId@word; value:tf


if __name__ == '__main__':
    run()
