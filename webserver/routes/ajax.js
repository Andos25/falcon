/*
ALL ajax request
*/
var mongoclient = require('../dbengine');
var express = require('express');
var fs = require('fs');
var path = require('path');
var exec = require("child_process").exec;
var zerorpc = require("zerorpc");
var cilent = new zerorpc.Client();
cilent.connect("tcp://127.0.0.1:4242");
app = express();
//dashboard
exports.select_sexinfo = function(req, res) {
  mongoclient.open(function(err, mongoclient) {
    var db = mongoclient.db("weibo");
    var collection = db.collection("provinces")
    var result = {};
    var malelist = new Array();
    var femalelist = new Array();
    var categories = new Array();
    var percentage = new Array();
    if (req.query.selectinfo == 0) {
      collection.find().limit(15).toArray(function(err, data) {
        var male = 0;
        var female = 0;
        for (var i in data) {
          male += data[i]["m"];
          female += data[i]["f"];
          malelist.push(0 - data[i]["m"]);
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
    } else {
      collection.findOne({
        "id": parseInt(req.query.selectinfo)
      }, function(err, data) {
        percentage.push(["male", data["m"]]);
        percentage.push(["female", data["f"]]);
        data = data["citys"]
        for (i in data) {
          malelist.push(0 - data[i]["m"]);
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

exports.select_popinfo = function(req, res) {
  mongoclient.open(function(err, mongoclient) {
    var db = mongoclient.db("weibo");
    var collection = db.collection("provinces")
    if (req.query.selectinfo == 0) {
      collection.find().toArray(function(err, data) {
        var result = new Array();
        for (var i in data) {
          result.push([data[i]["name"], data[i]["population"]]);
        }
        mongoclient.close();
        res.json(result);
      });
    } else {
      collection.find({
        "id": parseInt(req.query.selectinfo)
      }).toArray(function(err, data) {
        var result = new Array();
        data = data[0]["citys"];
        for (var i in data) {
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
//user
exports.user_register = function(req, res) {
  mongoclient.open(function(err, mongoclient) {
    var db = mongoclient.db("falcon");
    var collection = db.collection("users");
    var email = req.query.email;
    var passwd = req.query.password;
    var name = req.query.uname;
    collection.find({
      "email": email
    }).toArray(function(err, data) {
      if (data.length != 0) {
        var result = null;
        mongoclient.close();
        res.json(result);
      } else {
        collection.insert({
          "name": name,
          "email": email,
          "passwd": passwd
        }, {
          w: 1,
          safe: true
        }, function(err, result) {
          if (email == result[0]["email"]) {
            mongoclient.close();
            res.json(0);
          } else {
            mongoclient.close();
            res.json(1);
          }
        });
      }
    });
  });
}

exports.user_login = function(req, res) {
  mongoclient.open(function(err, mongoclient) {
    var db = mongoclient.db("falcon");
    var collection = db.collection("users");
    var email = req.query.email;
    var passwd = req.query.password.toString();
    collection.find({
      "email": email
    }).toArray(function(err, user) {
      mongoclient.close();
      if (user.length != 0 && user[0]["passwd"] == passwd) {
        // express.session({ user: user });
        req.session.user = user[0];
        result = 0;
        res.json(result);
        res.cookie("password", passwd);
      } else {
        result = 1;
        res.json(result);
      }
    });
  });
}

exports.user_old_passwd = function(req, res) {
  var user = req.session.user;
  mongoclient.open(function(err, mongoclient) {
    var db = mongoclient.db("falcon");
    var collection = db.collection("users");
    var passwd = req.query.password;
    collection.find({
      "email": user["email"]
    }).toArray(function(err, data) {
      if (data.length != 0 && data[0]["passwd"] == passwd.toString()) {
        result = 0;
        mongoclient.close();
        res.json(result);
      } else {
        result = 1;
        mongoclient.close();
        res.json(result);
      }
    });
  });
}

//return 1 when update sucess
exports.user_passwd_change = function(req, res) {
  var user = req.session.user;
  mongoclient.open(function(err, mongoclient) {
    var db = mongoclient.db("falcon");
    var collection = db.collection("users");
    var email = user["email"];
    var name = req.query.name;
    var passwd = req.query.password.toString();
    collection.update({
      "email": user["email"]
    }, {
      $set: {
        "name": name,
        "passwd": passwd
      }
    }, {
      w: 1
    }, function(err, result) {
      if (err) console.warn(err.message);
      console.log(result);
      mongoclient.close();
      res.json(result);
    });
  });
}

exports.user_name = function(req, res) {
  var user = req.session.user;
  console.log(user);
  res.json(user);
}




exports.user_logout = function(req, res) {
  req.session.user = null;
  res.json(0);
}

//sensitive
exports.sensitiveinfo = function(req, res) {
  mongoclient.open(function(err, mongoclient) {
    var db = mongoclient.db("weibo");
    var textcollection = db.collection("text");
    // var usercollection = db.collection("users");
    var everypage = parseInt(req.query.everypage);
    var pagecount = parseInt(req.query.pagecount);
    var result = new Array();
    textcollection.find({
      "text": {
        "$regex": '.*' + req.query.searchinfo + '.*'
      },
      "kwords": {
        "$exists": true
      }
    }).skip(everypage * pagecount).limit(everypage).toArray(function(err, data) {
      for (i in data) {
        tmp = {};
        tmp["user_id"] = data[i]["user_id"];
        tmp["text"] = data[i]["text"];
        tmp["kwords"] = data[i]["kwords"];
        result.push(tmp);
      }
      mongoclient.close();
      res.json(result);
    });
  });
}

//panel
exports.execute = function(req, res) {
  var str = fs.realpathSync('.');
  var location = path.dirname(str);
  location += "/algorithm/" + req.query.execute_type + "/run.sh";
  console.log(location);
  exec(location, function(error, stdout, stderr) {
    var pattern = new RegExp('completed successfully');
    res.cookie("execute_state", "");
    if (pattern.test(stdout) || pattern.test(stderr)) {
      res.json(true);
    } else {
      res.json(false);
    }
  });
}

exports.checkschedule = function(req, res) {
  cilent.invoke("checkschedule", function(error, response, more) {
    res.json(response);
  });
}

//emotion
exports.emotion = function(req, res) {
  mongoclient.open(function(err, mongoclient) {
    var db = mongoclient.db("weibo");
    var collection = db.collection("text");
    var result = [];
    collection.find({
      "em": 1
    }).count(function(err, data) {
      result.push(["positive", data]);
      collection.find({
        "em": 0
      }).count(function(err, data) {
        result.push(["mid", data]);
        collection.find({
          "em": -1
        }).count(function(err, data) {
          result.push(["negtive", data]);
          mongoclient.close();
          res.json(result);
        });
      });
    });
  });
}

exports.topologydata = function(req, res) {
  mongoclient.open(function(err, mongoclient) {
    var db = mongoclient.db("falcon");
    var collection = db.collection("craw");
    var name = req.query.username;
    console.log(name);
    collection.find({
      "name": name
    }).toArray(function(err, weibo) {
      mongoclient.close();
      if (weibo.length != 0) {
        var data = weibo[0]["content"];
        console.log(data);
        res.json(data);
      } else {
        console.log("crawling...........");
        res.json("0");
        cilent.invoke("weibocrawler", name, function(error, response, more) {});
      }
    });
  });
}

exports.cluster_data = function(req, res) {
  mongoclient.open(function(err, mongoclient) {
    var db = mongoclient.db("weibo");
    var collection = db.collection("cluster");
    collection.find({
      "blogsum": {
        $gt: 20
      }
    }).toArray(function(err, cluster) {
      var categories = new Array();
      var data = new Array();
      for (var i = 0; i < cluster.length; i++) {
        categories.push(cluster[i]["keyword"].toString());
        data.push(cluster[i]["blogsum"]);
      }
      result = {
        "categories": categories,
        "data": data
      };
      mongoclient.close();
      res.json(result);
    });
  });
}