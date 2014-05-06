function logout(){
  $.getJSON("/ajax/user_logout",{},function(result){
    if (result==0) 
      alert("Logout sucess");
    window.location="/"
  });
}