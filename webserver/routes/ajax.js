/*
ALL ajax request
*/
mongoclient = require('../dbengine');

//dashboard
exports.select_sexinfo = function(req, res){
  console.log(req.query.selectinfo);
  // mongoclient.open(function(err, mongoclient){
  //   var db = mongoclient.db("weibo");
  //   var collection = db.collection("")
  //   if(req.query.selectinfo == 0)
  //     mongoclient.close();
  //   });
  // });
}

exports.select_popinfo = function(req, res){
  mongoclient.open(function(err, mongoclient){
    var db = mongoclient.db("weibo");
    var collection = db.collection("provinces")
    console.log(req.query.selectinfo);
    if(req.query.selectinfo == 0){
      collection.find().toArray(function(err, data){
        var result = new Array();
        for(var i in data){
          
        }
        mongoclient.close();
        res.json();
      });
    }else{
      collection.find({"id":parseInt(req.query.selectinfo)}).toArray(function(err, data){
        var result = new Array();
        data = data[0]["citys"]
        for(var i in data){
          var item = new Array();
          for(var key in data[i]){
            item.push(data[i][key]);
          }
          result.push(item);
        }
        mongoclient.close();
        res.json(result);
      });
    }
      
  });
  } 
