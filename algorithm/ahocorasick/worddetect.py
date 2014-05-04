#!/usr/bin/env python
#coding=utf-8

import ahocorasick
import pymongo
import jieba

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
        tmp = list()
        flag = 0
        for match in tree.findall(item):
            word = item[match[0]:match[1]]
            if word.decode("utf-8") in words:
                tmp.append(word)
                flag = 1

        if flag==0:continue
        tmp = list(set(tmp))
        i["kwords"] = tmp
        textcollection.save(i)

if __name__ == '__main__':
    run()

