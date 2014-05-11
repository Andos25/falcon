#!/usr/bin/env python
#coding=utf-8

import pymongo
import jieba


def get_collection(name):
    conn = pymongo.Connection("localhost", 27017)
    return conn["weibo"][name]

def get_tfidflist(words, idfcollection, emotionwords):
    count = 0
    idflist = dict()
    wordlist = dict()
    for word in words:
        word = word.encode("utf-8")
        content = idfcollection.find_one({"word": word})
        # if word not in emotionwords:continue
        if content == None:continue
        count += 1
        idflist[word] = content
        if(wordlist.has_key(word)):
            wordlist[word] += 1
        else:
            wordlist[word] = 1
    count = float(count)
    resultlist = dict()
    for word in wordlist.keys():
        resultlist[idflist[word]["id"]] = wordlist[word]/count * idflist[word]["idf"] * 100
    return resultlist

def get_text():
    idfcollection = get_collection("idf")
    positive = [i.rstrip() for i in open("./data/pos").readlines()]
    negtive = [i.rstrip() for i in open("./data/neg").readlines()]
    resultlist = list()
    # positive = positive[:5]
    # negtive = negtive[:5]
    emotionwords = [i.rstrip() for i in open("./data/Vnegative").readlines()]
    emotionwords += [i.rstrip() for i in open("./data/Anegative").readlines()]
    emotionwords += [i.rstrip() for i in open("./data/Vpositive").readlines()]
    emotionwords += [i.rstrip() for i in open("./data/Apositive").readlines()]
    for text in positive:
        try:
            words = jieba.cut(text, cut_all=False)
        except:
            continue
        tfidflist = get_tfidflist(words, idfcollection, emotionwords)
        tmp = "+1 "
        for i in tfidflist.keys():
            tmp += str(i)+":"+str(tfidflist[i])+" "
        tmp += '\n'
        resultlist.append(tmp)

    for text in negtive:
        try:
            words = jieba.cut(text, cut_all=False)
        except:
            continue
        tfidflist = get_tfidflist(words, idfcollection, emotionwords)
        tmp = "-1 "
        for i in tfidflist.keys():
            tmp += str(i)+":"+str(tfidflist[i])+" "
        tmp += '\n'
        resultlist.append(tmp)

    f = open("tfidf", "w")
    f.writelines(resultlist)
    f.close()

if __name__ == '__main__':
    get_text()




 