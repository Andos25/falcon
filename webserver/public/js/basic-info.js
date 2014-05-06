  $(document).ready(function(){
    //change the icon name with get_username
      var uname = get_username();
  })
 function get_username(){
    $.getJSON("/ajax/user_name", {}, function(data) {
      return data;
      });
}
function logout(){
  $.getJSON("/ajax/user_logout",{},function(result){
    if (result==0) 
      alert("Logout sucess");
    window.location="/"
  });
}