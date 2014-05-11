/**
 * Module dependencies.
 */
var express = require('express');
var MongoStore = require('connect-mongo')(express);
var routes = require('./routes');
var user = require('./routes/user');
var ajax = require('./routes/ajax');
var http = require('http');
var path = require('path');
var nunjucks = require('nunjucks');
var app = express();

// nunjucks configure
nunjucks.configure('views', {
  autoescape: true,
  express: app,
  watch: true
});
// all environments
app.set('port', process.env.PORT || 3000);
app.set('views', path.join(__dirname, 'views'));
app.use(express.cookieParser());
app.use(express.session({
  secret: "falcon",
  store: new MongoStore({
    db: "falcon"
  })
}));
app.use(express.favicon());
app.use(express.logger('dev'));
app.use(express.json());
app.use(express.urlencoded());
app.use(express.methodOverride());
// app.use(express.cookieParser('your secret here'));
// app.use(express.session());
app.use(app.router);
app.use(express.static(path.join(__dirname, 'public')));

// development only
if ('development' == app.get('env')) {
  app.use(express.errorHandler());
}

//normal page
app.get('^/$', routes.index);
app.get('^/index$', routes.index);
app.get('^/dashboard', routes.dashboard);
app.get('^/files', routes.files);
app.get('^/blog-new', routes.emotion);
app.get('^/sensitive', routes.sensitive);
app.get('^/topology', routes.topology);
app.get('^/page-new', routes.panel);
app.get('^/retrieve', routes.retrieve);
app.get('^/register', routes.register);
app.get('^/userboard', routes.userboard);

//ajax request

//dashboard
app.get('^/ajax/dashboard_select_sexinfo/', ajax.select_sexinfo);
app.get('^/ajax/dashboard_select_popinfo/', ajax.select_popinfo);
//sensitive
app.get('^/ajax/sensitiveinfo/', ajax.sensitiveinfo);
//panel
app.get('^/ajax/panel_execute/', ajax.execute);
app.get('^/ajax/panel_checkschedule/', ajax.checkschedule);
//emotion
app.get('^/ajax/emotion/', ajax.emotion);

//user basic operate
app.get('^/ajax/user_register', ajax.user_register);
app.get('^/ajax/user_login', ajax.user_login);
app.get('^/ajax/user_old_passwd', ajax.user_old_passwd);
app.get('^/ajax/user_passwd_change', ajax.user_passwd_change);
app.get('^/ajax/user_name', ajax.user_name);
app.get('^/ajax/user_logout', ajax.user_logout);
app.get('^/ajax/topologydata',ajax.topologydata)

http.createServer(app).listen(app.get('port'), function() {
  console.log('Express server listening on port ' + app.get('port'));
});