mongoclient = require('../dbengine');
  mongoclient.open(function(err, mongoclient){
    var db = mongoclient.db("falcon");
    var collection = db.collection("users");
      collection.find({}, {w:1,safe:true}, function(err, data) {
          console.log(data);});
    });