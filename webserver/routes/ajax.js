/*
ALL ajax request
*/
mongoclient = require('../dbengine');
express = require('express');
app = express(); 
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

  exports.user_register = function(req, res){
  mongoclient.open(function(err, mongoclient){
    var db = mongoclient.db("falcon");
    var collection = db.collection("users");
    var email = req.query.email;
    var passwd = req.query.password;
      collection.find({"email":email}).toArray(function(err, data){
        if(data.length!=0){
              var result = 1;
              res.json(result);
          }else{
              collection.insert({"email": email,"passwd":passwd}, {w:1,safe:true}, function(err, data) {
                console.log();
                if(err){
                    // if (err && err.message.indexOf('E11000 ') !== -1) 
                        // this _id was already inserted in the database
                        console.log(data);
                        res.json(data);
                }
                else{
                  console.log(data);
                  res.json(data);
                }
          });
        }
        mongoclient.close();
      });
    });
  }

  exports.user_login = function(req, res){
  mongoclient.open(function(err, mongoclient){
    var db = mongoclient.db("falcon");
    var collection = db.collection("users");
    var email = req.query.email;
    var passwd = req.query.password.toString();
      collection.find({"email":email}).toArray(function(err, user){
        console.log(passwd);
        mongoclient.close();
        if(user.length != 0 && user[0]["passwd"]==passwd){
              // express.session({ user: user });
              req.session.user = user[0];
              result = 0;
              res.json(result);
          }else{
            result = 1;
            res.json(result);
        }
      });
    });
  }

exports.user_old_passwd = function(req, res){
  var user = req.session.user;
  mongoclient.open(function(err, mongoclient){
    var db = mongoclient.db("falcon");
    var collection = db.collection("users");
    var passwd = req.query.password;
      collection.find({"email":user["email"]}).toArray(function(err, data){
        if(data.length!=0 && data[0]["passwd"]==passwd.toString()){
              result = 0;
              res.json(result);
          }else{
            result = 1;
            res.json(result);
        }
        mongoclient.close();
      });
    });
  }


  exports.user_passwd_change = function(req, res){
  var user = req.session.user;
  mongoclient.open(function(err, mongoclient){
    var db = mongoclient.db("falcon");
    var collection = db.collection("users");
    var email = user["email"];
    var passwd = req.query.password.toString();
    collection.update({"email": user["email"]}, {$set: {"name":name,"passwd": passwd}}, {w:1}, function(err,result) {
      if (err) console.warn(err.message);
      console.log(result);
      res.json(result);
        });
      mongoclient.close();
      });
  }
  
  exports.user_name = function(req, res){
   res.json(req.session.user["name"]);
  }

