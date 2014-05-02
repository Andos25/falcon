var mongoclient = require('./dbengine');

  mongoclient.open(function(err, mongoclient){
    var db = mongoclient.db("weibo");
    var collection = db.collection("provinces")
    if(req.query.selectinfo == 0){
      collection.find().toArray(function(err, data){
        var result = new Array();
        for(var i in data){
          
        }
        mongoclient.close();
        res.json();
      });
    }else{
      collection.find({"id":req.query.selectinfo}).toArray(function(err, data){
        var result = new Array();
        data = data[0]["citys"]
        for(var i in data){
          result.push([data[i][1], data[i][0]])
        }
        
        res.json(result);
      });
    }
      
  });