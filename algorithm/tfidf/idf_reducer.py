#!/usr/bin/env python
#coding=utf-8

from operator import itemgetter
import sys
import math
from pymongo import *

##idf
def idf_reducer(ip, dbName, collectionName, fileSum):
    con = Connection(ip)
    db = con[dbName]
    collection = db[collectionName]

    word = None
    wordlist = dict()
    for line in sys.stdin:
        if "\t" in line:
            word, count = line.strip().split('\t', 1)
        if wordlist.has_key(word):
            wordlist[word] += 1
        else:
            wordlist[word] = 1
        for i in range(len(wordlist)):
            #rint 'word', wordlist.keys()[i], ' idf', math.log(fileSum/(wordlist.values()[i] + 1), 10)
            collection.save({'word':wordlist.keys()[i], 'idf':math.log(fileSum/(wordlist.values()[i] + 1), 10)})

if __name__ == '__main__':
    ip = 'localhost'
    dbName = 'weibo'
    collectionName = 'idf_test'
    fileSum = 50
    idf_reducer(ip, dbName, collectionName, fileSum)