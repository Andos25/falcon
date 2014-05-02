/*
ALL ajax request
*/
mongoclient = require('../dbengine');

//dashboard
exports.select_sexinfo = function(req, res){
  mongoclient.open(function(err, mongoclient){
    var db = mongoclient.db("weibo");
    var collection = db.collection("provinces")
    if(req.query.selectinfo == 0){
      collection.find().toArray(function(err, data){
        var result = new Array();
        var male = 0;
        var female = 0;
        for(var i in data){
          male += data[i]["m"];
          female += data[i]["f"];
        }
        result.push(["male", male]);
        result.push(["female", female]);
        mongoclient.close();
        res.json(result);
      });
    }else{
      collection.find({"id":parseInt(req.query.selectinfo)}).toArray(function(err, data){
        var result = new Array();
        data = data[0];
        result.push(["male", data["m"]]);
        result.push(["female", data["f"]]);
        mongoclient.close();
        res.json(result);
      });
    }
  });
}

exports.select_popinfo = function(req, res){
  mongoclient.open(function(err, mongoclient){
    var db = mongoclient.db("weibo");
    var collection = db.collection("provinces")
    if(req.query.selectinfo == 0){
      collection.find().toArray(function(err, data){
        var result = new Array();
        for(var i in data){
          var item = new Array();
          item.push(data[i]["name"]);
          item.push(data[i]["population"]);
          result.push(item);
        }
        mongoclient.close();
        res.json(result);
      });
    }else{
      collection.find({"id":parseInt(req.query.selectinfo)}).toArray(function(err, data){
        var result = new Array();
        data = data[0]["citys"];
        for(var i in data){
          var item = new Array();
          item.push(data[i]["cname"]);
          item.push(data[i]["population"]);
          result.push(item);
        }
        mongoclient.close();
        res.json(result);
      });
    }
  });
  } 
