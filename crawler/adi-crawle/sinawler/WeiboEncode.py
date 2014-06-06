#!/usr/bin/env python
#coding=utf8


'''''Author: Zheng Yi  
    Email: zhengyi.bupt@qq.com'''  
      
      
import urllib  
import base64  
import hashlib  
      
      
def PostEncode(userName, passWord, serverTime, nonce):  
        "Used to generate POST data"  
              
        encodedUserName = GetUserName(userName)  
        encodedPassWord = GetPassword(passWord, serverTime, nonce)  
        postPara = {  
            'entry': 'weibo',  
            'gateway': '1',  
            'from': '',  
            'savestate': '7',  
            'userticket': '1',  
            'ssosimplelogin': '1',  
            'vsnf': '1',  
            'vsnval': '',  
            'su': encodedUserName,  
            'service': 'miniblog',  
            'servertime': serverTime,  
            'nonce': nonce,  
            'pwencode': 'wsse',  
            'sp': encodedPassWord,  
            'encoding': 'UTF-8',  
            'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',  
            'returntype': 'META'  
        }  
        postData = urllib.urlencode(postPara)  
        return postData  
      
      
def GetUserName(userName):  
        "Used to encode user name"  
          
        userNameTemp = urllib.quote(userName)  
        userNameEncoded = base64.encodestring(userNameTemp)[:-1]  
        return userNameEncoded  
      
      
def GetPassword(passWord, serverTime, nonce):  
        "Used to encode user password"  
          
        pwdTemp1 = hashlib.sha1(passWord).hexdigest()  
        pwdTemp2 = hashlib.sha1(pwdTemp1).hexdigest()  
        pwdTemp3 = pwdTemp2 + serverTime + nonce  
        pwdEncoded = hashlib.sha1(pwdTemp3).hexdigest()  
        return pwdEncoded  
