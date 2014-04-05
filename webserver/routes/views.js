
/*
 * GET home page.
 */

exports.index = function(req, res){
  res.render('index.html');
};

exports.dashboard = function(req, res){
  console.log("dashboard");
  res.render('dashboard.html');
};

exports.files = function(req, res){
  res.render('files.html');
};

exports.blog= function(req, res){
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