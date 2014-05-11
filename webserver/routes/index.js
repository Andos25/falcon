/*
 * GET home page.
 */
mongoclient = require('../dbengine');
exports.index = function(req, res) {
  res.render('index.html');
};

exports.dashboard = function(req, res) {
  if (!req.session.user) {
    return res.redirect('/');
  }
  mongoclient.open(function(err, mongoclient) {
    var db = mongoclient.db("weibo");
    var selectitems = new Array();
    var textcount;
    var userscount;
    // var user = req.session.user;
    var username = req.session.user["name"];
    db.collection('provinces').find().toArray(function(err, data) {

      selectitems.push([0, "全国"]);
      for (i in data) {
        var item = new Array();
        item.push(data[i]["id"]);
        item.push(data[i]["name"]);
        selectitems.push(item);
      }
      db.collection('text').count(function(err, data) {
        textcount = data;
        db.collection('users').count(function(err, data) {
          userscount = data;
          mongoclient.close();
          res.render('dashboard.html', {
            "selectitems": selectitems,
            "textcount": textcount,
            "userscount": userscount,
            "username": username
          });
        });
      });
    });
  });
};

exports.files = function(req, res) {
  if (!req.session.user) {
    return res.redirect('/');
  }
  var username = req.session.user["name"];
  res.render('files.html',{"username":username});
};

exports.emotion = function(req, res) {
  if (!req.session.user) {
    return res.redirect('/');
  }
  return res.render("emotion.html");
};

exports.sensitive = function(req, res) {
  if (!req.session.user) {
    return res.redirect('/');
  }
  var username = req.session.user["name"];
  res.render('sensitive.html',{"username":username});
};

exports.topology = function(req, res) {
  if (!req.session.user) {
    return res.redirect('/');
  }
  var username = req.session.user["name"];
  res.render('topology.html',{"username":username});
};
exports.panel = function(req, res) {
  if (!req.session.user) {
    return res.redirect('/');
  }
  var username = req.session.user["name"];
  res.render('panel.html',{"username":username});
};

exports.retrieve = function(req, res) {
  if (!req.session.user) {
    return res.redirect('/');
  }
  res.render('retrieve.html');
};
exports.register = function(req, res) {
  res.render('register.html');
};
exports.userboard = function(req, res) {
  if (!req.session.user) {
    return res.redirect('/');
  }
  var username = req.session.user["name"];
  res.render('userboard.html');
};