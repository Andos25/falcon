$(document).ready(function() {

  if (checkCookie()) {
    $("button").attr("disabled", true);
    var execute_state = getCookie("execute_state");
    count(execute_state);
    checkschedule(execute_state);
    $("span#" + execute_state).text("Running");
    document.getElementsByName(execute_state)[0].show(700);
  }
  $("div#block").hide();
  $("button").click(function() {
    var result = confirm("are you sure to begin this execute?");
    if (result == true) {
      $(this).parent().children("#block").show(700);
      $("button").attr("disabled", "true");
      $(".mapreduce").html("");
      $("span#" + this.name).text("Running");
      setCookie("execute_state", this.name);
      var now = new Date();
      addCookie("begin_time", now.getTime());
      execute(this.name);
    } else {
      return;
    }
  });
});
var state = {
  "statistics": true,
  "ahocorasick": true,
  "tfidf": true,
  "kmeans": true,
  "emotion": true
}
var schedule = {
  "statistics": 0,
  "ahocorasick": 0,
  "tfidf": 0,
  "kmeans": 0,
  "emotion": 0
}

  function getCookie(c_name) {
    if (document.cookie.length > 0) {
      c_start = document.cookie.indexOf(c_name + "=")
      if (c_start != -1) {
        c_start = c_start + c_name.length + 1
        c_end = document.cookie.indexOf(";", c_start)
        if (c_end == -1) c_end = document.cookie.length
        return unescape(document.cookie.substring(c_start, c_end))
      }
    }
    return ""
  }

  function setCookie(c_name, value) {
    document.cookie = c_name + "=" + escape(value);
  }

  function addCookie(c_name, value) {
    document.cookie += ("&" + c_name + "=" + escape(value));
  }

  function checkCookie() {
    execute_state = getCookie('execute_state')
    console.log(execute_state);
    if (execute_state != null && execute_state != "") {
      return true;
    } else {
      return false;
    }
  }

var execute = function(execute_type) {
  state[execute_type] = true;
  count(execute_type);
  checkschedule(execute_type);
  $.getJSON("/ajax/panel_execute/", {
      "execute_type": execute_type
    },
    function(data) {
      setCookie("execute_state", "");
      if (!data) {
        state[execute_type] = false;
      }
    }
  )
};

var checkschedule = function(execute_type) {
  $.getJSON("/ajax/panel_checkschedule/", {}, function(data) {
    data = parseInt(data);
    var now = new Date();
    var begin_time = parseInt(getCookie("begin_time"));
    if (data != -1) {
      schedule[execute_type] = data;
    } else if (schedule[execute_type] != 0 || now.getTime() - begin_time > 60000) {
      setCookie("execute_state", "");
    }
    if (checkCookie())
      setTimeout(function() {
        checkschedule(execute_type);
      }, 1500);
  });
}

var count = function(name) {
  if (isCanvasSupported) {
    var c = document.createElement('canvas');
    c.width = 650;
    c.height = 25;
    var cw = c.width;
    var ch = c.height;
    document.getElementById(name + "bar").appendChild(c);

    var cl = new lightLoader(c, cw, ch, name);

    setupRAF();
    cl.init();
  }
}

// var btnStart = document.getElementById("start");
// btnStart.onclick = function() {
// flagEnd = true;

// };

// var btnEnd = document.getElementById("stop");
// btnEnd.onclick = function() {
//   flagEnd = false;
// };

/*========================================================*/
/* Light Loader
/*========================================================*/
var lightLoader = function(c, cw, ch, execute_type) {

  var _this = this;
  this.execute_type = execute_type;
  this.c = c;
  this.ctx = c.getContext('2d');
  this.cw = cw;
  this.ch = ch;

  this.loaded = 0;
  this.loaderSpeed = .6;
  this.loaderHeight = 20;
  this.loaderWidth = 620;
  this.loader = {
    x: (this.cw / 2) - (this.loaderWidth / 2),
    y: (this.ch / 2) - (this.loaderHeight / 2)
  };
  this.particles = [];
  this.particleLift = 180;
  this.hueStart = 0
  this.hueEnd = 120;
  this.hue = 0;
  this.gravity = .15;
  this.particleRate = 4;

  /*========================================================*/
  /* Initialize
  /*========================================================*/
  this.init = function() {
    this.loop();
  };

  /*========================================================*/
  /* Utility Functions
  /*========================================================*/
  this.rand = function(rMi, rMa) {
    return~~ ((Math.random() * (rMa - rMi + 1)) + rMi);
  };
  this.hitTest = function(x1, y1, w1, h1, x2, y2, w2, h2) {
    return !(x1 + w1 < x2 || x2 + w2 < x1 || y1 + h1 < y2 || y2 + h2 < y1);
  };

  /*========================================================*/
  /* Update Loader
  /*========================================================*/
  this.updateLoader = function() {
    if (checkCookie()) {
      this.loaded = schedule[this.execute_type];
    } else {
      this.loaded = 100;
      $("button").removeAttr("disabled");
      $("span#" + this.execute_type).text(state[this.execute_type] ? "Finished" : "Error");
    }
  };

  /*========================================================*/
  /* Render Loader
  /*========================================================*/
  this.renderLoader = function() {
    this.ctx.fillStyle = '#000';
    this.ctx.fillRect(this.loader.x, this.loader.y, this.loaderWidth, this.loaderHeight);

    this.hue = this.hueStart + (this.loaded / 100) * (this.hueEnd - this.hueStart);

    var newWidth = (this.loaded / 100) * this.loaderWidth;
    this.ctx.fillStyle = 'hsla(' + this.hue + ', 100%, 40%, 1)';
    this.ctx.fillRect(this.loader.x, this.loader.y, newWidth, this.loaderHeight);

    this.ctx.fillStyle = '#222';
    this.ctx.fillRect(this.loader.x, this.loader.y, newWidth, this.loaderHeight / 2);
  };

  /*========================================================*/
  /* Particles
  /*========================================================*/
  this.Particle = function() {
    this.x = _this.loader.x + ((_this.loaded / 100) * _this.loaderWidth) - _this.rand(0, 1);
    this.y = _this.ch / 2 + _this.rand(0, _this.loaderHeight) - _this.loaderHeight / 2;
    this.vx = (_this.rand(0, 4) - 2) / 100;
    this.vy = (_this.rand(0, _this.particleLift) - _this.particleLift * 2) / 100;
    this.width = _this.rand(1, 4) / 2;
    this.height = _this.rand(1, 4) / 2;
    this.hue = _this.hue;
  };

  this.Particle.prototype.update = function(i) {
    this.vx += (_this.rand(0, 6) - 3) / 100;
    this.vy += _this.gravity;
    this.x += this.vx;
    this.y += this.vy;

    if (this.y > _this.ch) {
      _this.particles.splice(i, 1);
    }
  };

  this.Particle.prototype.render = function() {
    _this.ctx.fillStyle = 'hsla(' + this.hue + ', 100%, ' + _this.rand(50, 70) + '%, ' + _this.rand(20, 100) / 100 + ')';
    _this.ctx.fillRect(this.x, this.y, this.width, this.height);
  };

  this.createParticles = function() {
    var i = this.particleRate;
    while (i--) {
      this.particles.push(new this.Particle());
    };
  };

  this.updateParticles = function() {
    var i = this.particles.length;
    while (i--) {
      var p = this.particles[i];
      p.update(i);
    };
  };

  this.renderParticles = function() {
    var i = this.particles.length;
    while (i--) {
      var p = this.particles[i];
      p.render();
    };
  };


  /*========================================================*/
  /* Clear Canvas
  /*========================================================*/
  this.clearCanvas = function() {
    this.ctx.globalCompositeOperation = 'source-over';
    this.ctx.clearRect(0, 0, this.cw, this.ch);
    this.ctx.globalCompositeOperation = 'lighter';
  };

  /*========================================================*/
  /* Animation Loop
  /*========================================================*/
  this.loop = function() {
    var loopIt = function() {
      requestAnimationFrame(loopIt, _this.c);
      _this.clearCanvas();

      _this.createParticles();

      _this.updateLoader();
      _this.updateParticles();

      _this.renderLoader();
      _this.renderParticles();

    };
    loopIt();
  };

};

/*========================================================*/
/* Check Canvas Support
/*========================================================*/
var isCanvasSupported = function() {
  var elem = document.createElement('canvas');
  return !!(elem.getContext && elem.getContext('2d'));
};

/*========================================================*/
/* Setup requestAnimationFrame
/*========================================================*/
var setupRAF = function() {
  var lastTime = 0;
  var vendors = ['ms', 'moz', 'webkit', 'o'];
  for (var x = 0; x < vendors.length && !window.requestAnimationFrame; ++x) {
    window.requestAnimationFrame = window[vendors[x] + 'RequestAnimationFrame'];
    window.cancelAnimationFrame = window[vendors[x] + 'CancelAnimationFrame'] || window[vendors[x] + 'CancelRequestAnimationFrame'];
  };

  if (!window.requestAnimationFrame) {
    window.requestAnimationFrame = function(callback, element) {
      var currTime = new Date().getTime();
      var timeToCall = Math.max(0, 16 - (currTime - lastTime));
      var id = window.setTimeout(function() {
        callback(currTime + timeToCall);
      }, 1500);
      lastTime = currTime + timeToCall;
      return id;
    };
  };

  if (!window.cancelAnimationFrame) {
    window.cancelAnimationFrame = function(id) {
      clearTimeout(id);
    };
  };
};