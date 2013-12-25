from weibo import APIClient
import urllib, httplib

client_id = '1000570550' # app key
app_scret = 'aff4f0ce3b15153bb755042dccb3a922' # app secret
redirect_uri = 'http://www.data-god.com'
username = "h.chujieandos@gmail.com"
passwd = "antonidas25"

# code = your.web.framework.request.get('code')
# client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
class Crawler():
    def __init__(self, client_id, redirect_uri, username, passwd):
        url = "https://api.weibo.com/oauth2/authorize?client_id="+client_id+"&redirect_uri="+redirect_uri+"&response_type=code"
        conn = httplib.HTTPSConnection("api.weibo.com")
        postdata = urllib.urlencode({'client_id':client_id,'redirect_uri':redirect_uri,'action':'submit','userId':username,'passwd':passwd})
        conn.request('POST','/oauth2/authorize',postdata,{'Referer':url, 'Content-Type': 'application/x-www-form-urlencoded'})
        res = conn.getresponse()
        page = res.read()
        code = res.msg['Location'].split("?")[1][5:]
        self.client = APIClient(app_key=client_id, app_secret=app_scret, redirect_uri=redirect_uri)
        r = self.client.request_access_token(code)
        self.access_token = r.access_token
        # expires_in = r.expires_in
        self.client.set_access_token(r.access_token, r.expires_in)

    def users_show(self, user_id):
        print self.client.users.show.get(uid=user_id)

    def friendships_followers_active(self, user_id):
        print self.client.friendships.followers.active.get(uid = user_id)

    def statuses_user_timeline(self, user_id):
        print self.client.statuses.user_timeline.get(uid = user_id, page = 1)

    def statuses_go(self, user_id):
        print self.client.statuses.go.get(uid = user_id)

if __name__ == '__main__':
    c = Crawler(client_id, redirect_uri, username, passwd)
    c.statuses_go(1867237712)

