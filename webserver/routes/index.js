
/*
 * GET home page.
 */
mongoclient = require('../dbengine');
exports.index = function(req, res){
  
  res.render('index.html');
};

exports.dashboard = function(req, res){
  mongoclient.open(function(err, mongoclient){
    var db = mongoclient.db("weibo");
    db.collection('provinces').find().toArray(function(err, data) {
      var selectitems = new Array();
      selectitems.push([0,"全国"]);
      for(i in data){
        var item = new Array();
        item.push(data[i]["id"]);
        item.push(data[i]["name"]);
        selectitems.push(item);
      }
        var collection1 = db.collection('provinces');
        collection1.count(function(err, count) {
          var provnum = count;
          var collection2 = db.collection('users');
          collection2.count(function(err, count) {
            var usernum = count;
            var collection3 = db.collection('text');
            collection3.count(function(err, count) {
              var textnum = count;
              var sum = textnum+usernum+provnum;
              res.render("dashboard.html", {"selectitems":selectitems,"sum":sum,"usernum":usernum,"textnum":textnum,"provnum":provnum});
              mongoclient.close();
            });
         });
       });
     });
    });
  };

exports.files = function(req, res){
  res.render('files.html');
};

exports.blog = function(req, res){
  res.render('blog.html');
};

exports.users = function(req, res){
  res.render('users.html');
};

exports.topology = function(req, res){
  res.render('topology.html');
};

exports.page = function(req, res){
  res.render('page.html');
};