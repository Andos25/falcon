#!/usr/bin/env python
#coding=utf-8

import ahocorasick
import pymongo
import jieba
import json

def get_collection(name):
    conn = pymongo.Connection("localhost", 27017)
    return conn["weibo"][name]

def run():
    collection = get_collection("keywords")
    textcollection = get_collection("text")
    tree = ahocorasick.KeywordTree()

    for i in collection.find():
        tree.add(i["word"].encode("utf-8"))
    tree.make()
    for i in textcollection.find():
        item = i["text"].encode("utf-8")
        try:
            words = jieba.cut(item, cut_all=False)
        except:
            continue
        ac = list()
        cutwords = list()
        for match in tree.findall(item):
            word = item[match[0]:match[1]]
            ac.append(word.decode("utf-8"))
        if(len(ac)==0):
            continue
        for word in words:
            cutwords.append(word)
        string = str(i["_id"])+"\t"+json.dumps({"ac": ac, "cutwords": cutwords})
        print string

        # if flag==0:continue
        # ac = list(set(ac))
        # i["kwords"] = ac
        # textcollection.save(i)

if __name__ == '__main__':
    run()

