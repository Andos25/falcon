
var mongodb = require("mongodb"),
  mongoserver = new mongodb.Server('localhost', 27017 ),
  mongodb =  new mongodb.Db('weibo', mongoserver, {safe:false});
  //console.log(mongodb);
  mongodb.open(function(err, db) {
  if (err) {
    return callback(err);
  }
  // 讀取 posts 集合
  db.collection('provinces', function(err, collection) {
  if (err) {
    mongodb.close();
    return callback(err);
  }
// 查找 user 屬性爲 username 的文檔，如果 username 是 null 則匹配全部
  collection.find().sort({time: -1}).toArray(function(err, docs) {
    console.log(docs)
    mongodb.close();
    if (err) {
      callback(err, null);
    }
    });
  });
});
