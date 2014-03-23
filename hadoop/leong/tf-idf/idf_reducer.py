#!/usr/bin/env python
#coding=utf-8

from operator import itemgetter
import sys
import math
from pymongo import *

##idf
con = Connection()
db = con.weibo
collection = db.idftest

# current_word = None
# current_count = 0
word = None

wordslist = dict()
for line in sys.stdin:
    line = line.strip()
    word, count = line.split('\t', 1)
    # try:
    #     count = int(count)
    # except ValueError:
    #     continue

    if wordslist.has_key(word):
        wordslist[word] += 1  #key: weibo text word ;value: how many times this word appears in all weibo texts
    else:
        wordslist[word] = 1
for i in range(len(wordslist)):
    collection.save({'word':wordslist.keys()[i], 'idf':math.log(50.0/(wordslist.values()[i] + 1), 10)})
    # print wordslist.keys()[i], math.log(50.0/(wordslist.values()[i] + 1), 10)

    # if current_word == word:
    #     current_count += count
    # else:
    #     if current_word:
    #         print '%s\t%s' %(current_word, current_count)
    #     current_count = count
    #     current_word = word

    # if current_word == word:
    #     print '%s\t%s' % (current_word, current_count)