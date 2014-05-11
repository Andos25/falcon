$(document).ready(function() {
  $("li#4").addClass('section');
  getsensitiveinfo(0);
});
var getsensitiveinfo = function(pagecount) {
  everypage = $("input#everypage").val();
  if (!everypage)
    everypage = 10;
  if (everypage <= 0) {
    alert("每页显示条目数设置非法,应为大于0的整数");
    return;
  }
  $.getJSON("/ajax/sensitiveinfo/", {
    "searchinfo": $("input#searchinfo").val(),
    "pagecount": pagecount,
    "everypage": everypage
  }, function(data) {
    var string = "";
    for (i in data) {
      var tmp = data[i]["kwords"].join("&nbsp&nbsp");
      string += "<tr><td>" + data[i].user_id + "</td><td>" + data[i].text + "</td><td>" + tmp + "</td></tr>";
    }
    $("#sensitiveinfo").html(string);
    nextpage = pagecount + 1;
    lastpage = pagecount - 1;
    if (pagecount == 0)
      button = "<button class=\"btn\" onclick=\"getsensitiveinfo(nextpage)\">下一页</button>";
    else
      button = "<button class=\"btn\" onclick=\"getsensitiveinfo(lastpage)\">上一页</button>&nbsp&nbsp&nbsp&nbsp&nbsp<button class=\"btn\" onclick=\"getsensitiveinfo(nextpage)\">下一页</button>";
    $('div#button').html(button);
  });
}