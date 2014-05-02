var dbsetting = require('./settings')

var server_options={'auto_reconnect':true,poolSize:5};
var MongoClient = require('mongodb').MongoClient,
    Server = require('mongodb').Server;
module.exports = new MongoClient(new Server(dbsetting.HOST, 27017), {native_parser: true});


// mongoclient.open(function(err, mongoclient) {


//       var db2 = mongoclient.db("weibo");
//       db2.collection('provinces').find().toArray(function(err, data) {

//         mongoclient.close();
//         console.log("closed");
//       });
//     });


  //   db = db.open(function(err, db) {
  //   if (err) {
  //     return console.log(err);
  //   }
  //   db.collection('provinces', function(err, collection) {
  //   if (err) {
  //     db.close();
  //     return console.log(err);
  //   }
  //   collection.find().toArray(function(err, docs) {
  //     console.log(docs[1])
  //     db.close();
  //     if (err) {
  //       callback(err, null);
  //     }
  //     });
  //   });
  // });
    
    
