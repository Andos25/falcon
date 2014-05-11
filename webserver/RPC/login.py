#coding=utf8
import urllib
import urllib2
import cookielib
import base64
import re
import rsa
import json
import hashlib
import binascii

#获取一个保存cookie的对象
cj = cookielib.LWPCookieJar()
#将一个保存cookie对象，和一个HTTP的cookie的处理器绑定
cookie_support = urllib2.HTTPCookieProcessor(cj)
#创建一个opener，将保存了cookie的http处理器，还有设置一个handler用于处理http的URL的打开
opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
#将包含了cookie、http处理器、http的handler的资源和urllib2对象板顶在一起
urllib2.install_opener(opener)


def get_servertime():
    url = 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=&rsakt=mod&client=ssologin.js(v1.4.15)&_=1399480145262'# HTTP/1.1
    data = urllib2.urlopen(url).read()
    # print data
    p = re.compile('\((.*)\)') 
    try:
        json_data = p.search(data).group(1)
        data = json.loads(json_data)
        servertime = str(data['servertime'])
        nonce = data['nonce']
        pubkey = data['pubkey']
        rsakv = data['rsakv']
        # print pubkey
        # print rsakv
        # print servertime
        # print nonce 
        return servertime, nonce,pubkey,rsakv
    except:
        print 'Get severtime error!' 
        return None

def get_pwd(pwd, servertime, nonce,pubkey):
    # pwd1 = hashlib.sha1(pwd).hexdigest()
    # pwd2 = hashlib.sha1(pwd1).hexdigest()
    # pwd3_ = pwd2 + servertime + nonce
    # pwd3 = hashlib.sha1(pwd3_).hexdigest()
    rsaPublickey = int(pubkey, 16)
    key = rsa.PublicKey(rsaPublickey, 65537) #创建公钥
    message = str(servertime) + '\t' + str(nonce) + '\n' + str(pwd)  #拼接明文 js加密文件中得到
    passwd = rsa.encrypt(message, key) #加密
    pwd3 = binascii.b2a_hex(passwd) #将加密信息转换为16进制。
    return pwd3

def get_user(username):
    username_ = urllib.quote(username)
    username = base64.encodestring(username_)[:-1] 
    return username

def weiboLogin():
    print "step into login"
    username = '15056012759'#微博账号
    pwd = '650913'#微博密码
    url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.15) '
    postdata = {
        'entry': 'weibo',
        'gateway': '1',
        'from': '',
        'savestate': '7',
        'userticket': '1',
        'ssosimplelogin': '1',
        'pagerefer' : 'http://login.sina.com.cn/sso/logout.php?entry=miniblog&r=http%3A%2F%2Fweibo.com%2Flogout.php%3Fbackurl%3D%252F',
        'vsnf': '1',
        'vsnval': '',
        'su' :'', # null in old
        'service': 'miniblog',
        'servertime': '',
        'nonce':'',  #null in old 
        'pwencode': 'rsa2',
        'rsakv':'',
        'sp': '',
        'encoding': 'UTF-8',
        'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
        'returntype': 'META'
} 
    try:
        servertime, nonce, pubkey, rsakv= get_servertime()
        # print servertime, nonce, pubkey, rsakv
    except:
        print 'error'
        return  postdata  #global
    postdata['servertime'] = servertime
    postdata['nonce'] = nonce
    postdata['rsakv'] = rsakv
    postdata['su'] = get_user(username)
    postdata['sp'] = get_pwd(pwd, servertime, nonce,pubkey)
    postdata = urllib.urlencode(postdata)
    headers = {          
          "domain": "widget.weibo.com",
          "hostOnly": "true",
          "httpOnly": "false",
          "name": "HAVAR",
          "path": "/",
          "secure": "false",
          "session": "true",
          "storeId": "0",
          "value": "wbvt_13182",
          'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:28.0) Gecko/20100101 Firefox/28.0'}
    # print postdata;
    #其实到了这里，已经能够使用urllib2请求新浪任何的内容了，这里已经登陆成功了
    req  = urllib2.Request(
        url = url,
        data = postdata,
        headers = headers
    )
    result = urllib2.urlopen(req)
    text = result.read()
    p = re.compile("location\.replace\(\'(.*?)\'\)") 
    try:
        login_url = p.search(text).group(1)
        urllib2.urlopen(login_url)
        # print cj._cookies.values()
        print "login success"
    except:
        print 'Login error!'
if __name__ == '__main__':
        weiboLogin()
        
