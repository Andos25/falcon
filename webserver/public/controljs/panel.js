$(document).ready(function() {
  // $("div#block").hide();
  $("button").click(function() {
    var result = confirm("are you sure to begin this execute?");
    if (result == true) {
      // $(this).parent().children("#block").show(700);
      $("span#" + this.name).text("Running");
      execute(this.name);
    } else {
      return;
    }
  });
});

var execute = function(execute_type) {
  flag[execute_type] = true;
  count(execute_type);
  $.getJSON("/ajax/panel_execute/", {
      "execute_type": execute_type
    },
    function(data) {
      flag[execute_type] = false;
    }
  )
};

var flag = {
  "statistics": true,
  "ahocorasick": true,
  "tfidf": true,
  "kmeans": true
}

var count = function(name) {
  console.log(name);
  var bar = $("#" + name + "bar");
  if (bar.width() < bar.parent().width()) {
    bar.width(function(i, orginValue) {
      //alert(orginValue);
      // console.log(i);
      setTimeout(function() {
        count(name)
      }, 50);
      return orginValue + 500;

    });
  } else if (flag[name]) {
    bar.width(function(i, orginValue) {
      setTimeout(function() {
        count(name)
      }, 1000);
      return 0;
    });
  } else {
    $("span#" + name).text("Finished");
  }
}
// function setCookie(c_name, value, expiredays) {
//   var exdate = new Date()
//   exdate.setDate(exdate.getDate() + expiredays)
//   document.cookie = c_name + "=" + escape(value) +
//     ((expiredays == null) ? "" : ";expires=" + exdate.toGMTString())
// }

// function getCookie(c_name) {
//   if (document.cookie.length > 0) {
//     c_start = document.cookie.indexOf(c_name + "=")
//     if (c_start != -1) {
//       c_start = c_start + c_name.length + 1
//       c_end = document.cookie.indexOf(";", c_start)
//       if (c_end == -1) c_end = document.cookie.length
//       return unescape(document.cookie.substring(c_start, c_end))
//     }
//   }
//   return ""
// }

// function checkCookie() {
//   username = getCookie('username')
//   if (username != null && username != "") {
//     alert('Welcome again ' + username + '!')
//   } else {
//     username = prompt('Please enter your name:', "")
//     if (username != null && username != "") {
//       setCookie('username', username, 365)
//     }
//   }
// }