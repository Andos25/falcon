CREATE TABLE hive_mongo
(id string,uid string,uname string,fansid string,fansname string)
STORED BY 'com.mongodb.hadoop.hive.MongoStorageHandler'
WITH SERDEPROPERTIES('mongo.columns.mapping'='{"id":"_id","uid":"uid","uname":"uname","fansid":"fansid","fansname":"fansname"}')
TBLPROPERTIES('mongo.uri'='mongodb://localhost:27017/sina.fans');

CREATE TABLE weibo_text
(id string,favorited boolean,user_id string,truncated boolean,text string,created_at string,source string)
   STORED BY 'com.mongodb.hadoop.hive.MongoStorageHandler'
   WITH SERDEPROPERTIES('mongo.columns.mapping'='{"id":"_id","favorited":"favorited","user_id":"user_id","truncated":"truncated","text":"text","created_at":"created_at","source":"source"}')
   TBLPROPERTIES('mongo.uri'='mongodb://localhost:27017/falcon.text');

{ "_id" : 78655, "favorited" : false, "user_id" : 1786562297, "truncated" : false, "text" : "奇怪的人", "created_at" : ISODate("2010-08-13T17:17:49Z"), "source" : "天翼社区" }


CREATE TABLE weibo_users
(id int,province string, city string,domain string,statuses_count int,name string,friends_count int,url string,gender string,created_at string,verified boolean,profile_image_url string,followers_count int,location string,favourites_count int)
   STORED BY 'com.mongodb.hadoop.hive.MongoStorageHandler'
   WITH SERDEPROPERTIES('mongo.columns.mapping'='{"id":"_id","province":"province","city":"city","domain": "domain","statuses_count":"statuses_count","name":"name","friends_count":"friends_count","url":"url","gender":"gender","created_at":"created_at","verified":"verified","profile_image_url":"profile_image_url","followers_count":"followers_count","location":"location","favourites_count":"favourites_count"}')
   TBLPROPERTIES('mongo.uri'='mongodb://localhost:27017/falcon.users');

{ "_id" : 10430, "province" : "11", "city" : "2", "domain" : "helor", "statuses_count" : 626, "name" : "helor", "friends_count" : 64, "url" : "http://blog.sina.com.cn/helor", "gender" : "m", "created_at" : ISODate("2009-10-30T00:00:00Z"), "verified" : false, "profile_image_url" : "http://tp3.sinaimg.cn/10430/50/1288597526/1", "followers_count" : 99, "location" : "北京 西城区", "favourites_count" : 2 }
