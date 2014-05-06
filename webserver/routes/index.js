/*
 * GET home page.
 */
mongoclient = require('../dbengine');
exports.index = function(req, res) {
  res.render('index.html');
};

exports.dashboard = function(req, res) {
  var user = req.session.user;
  mongoclient.open(function(err, mongoclient) {
    var db = mongoclient.db("weibo");
    var selectitems = new Array();
    var textcount;
    var userscount;
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
          if (!req.session.user) {
            return res.redirect('/');
          }
          res.render('dashboard.html', {
            "selectitems": selectitems,
            "textcount": textcount,
            "userscount": userscount
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
  res.render('files.html');
};

exports.blog = function(req, res) {
  if (!req.session.user) {
    return res.redirect('/');
  }
  res.render('blog.html');
};

exports.sensitive = function(req, res) {
  if (!req.session.user) {
    return res.redirect('/');
  }

  res.render('sensitive.html');
};

exports.topology = function(req, res) {
  if (!req.session.user) {
    return res.redirect('/');
  }
  res.render('topology.html');
};
exports.panel = function(req, res) {
  res.render('panel.html');
  exports.page = function(req, res) {
    if (!req.session.user) {
      return res.redirect('/');
    }
    res.render('page.html');
  };
  exports.retrieve = function(req, res) {
    if (!req.session.user) {
      return res.redirect('/');
    }
    res.render('retrieve.html');
  };
  exports.register = function(req, res) {
    if (!req.session.user) {
      return res.redirect('/');
    }
    res.render('register.html');
  };
  exports.userboard = function(req, res) {
    if (!req.session.user) {
      return res.redirect('/');
    }
    res.render('userboard.html');
  };