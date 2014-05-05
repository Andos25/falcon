mongoclient = require('../dbengine');
  mongoclient.open(function(err, mongoclient){
    var db = mongoclient.db("falcon");
    var collection = db.collection("users");
      collection.insert({"email": "1004060385@qq.com","passwd":"111111"}, {w:1,safe:true}, function(err, data) {
        if(err)
        console.warn(err.message);
        else
          console.log(data);});
    });