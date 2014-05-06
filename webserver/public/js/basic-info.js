  $(document).ready(function(){
    //change the icon name with get_username
      var uname = get_username();
      $('img').html('<span >Welcome back "uname" he</span>');
  })
 function get_username(){
    $.getJSON("/ajax/user_name", {}, function(data) {
      return data;
      });
}