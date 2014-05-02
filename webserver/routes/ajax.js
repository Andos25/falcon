/*
ALL ajax request
*/
mongoclient = require('../dbengine');

//dashboard
exports.select_sexinfo = function(req, res){
  mongoclient.open(function(err, mongoclient){
    var db = mongoclient.db("weibo");
    var collection = db.collection("provinces")
    var result = {};
    var malelist = new Array();
    var femalelist = new Array();
    var categories = new Array();
    var percentage = new Array();
    if(req.query.selectinfo == 0){
      collection.find().limit(15).toArray(function(err, data){
        var male = 0;
        var female = 0;
        for(var i in data){
          male += data[i]["m"];
          female += data[i]["f"];
          malelist.push(0-data[i]["m"]);
          femalelist.push(data[i]["f"]);
          categories.push(data[i]["name"]);
        }
        percentage.push(["male", male]);
        percentage.push(["female", female]);
        result["percentage"] = percentage;
        result["categories"] = categories;
        result["malelist"] = malelist;
        result["femalelist"] = femalelist;
        mongoclient.close();
        res.json(result);
      });
    }else{
      collection.findOne({"id":parseInt(req.query.selectinfo)}, function(err, data){
        percentage.push(["male", data["m"]]);
        percentage.push(["female", data["f"]]);
        data = data["citys"]
        for(i in data){
          malelist.push(0-data[i]["m"]);
          femalelist.push(data[i]["f"]);
          categories.push(data[i]["cname"]);
        }

        result["percentage"] = percentage;
        result["categories"] = categories;
        result["malelist"] = malelist;
        result["femalelist"] = femalelist;
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
          result.push([data[i]["name"], data[i]["population"]]);
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
