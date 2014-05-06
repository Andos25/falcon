//register.html js code 
function reg_checkname(){
    email=$("#name").val();
    if(email==""){
      $('div#checkname').html("<span style=\"color:white\">name can't be empty</span>");
    }
  }
 function reg_checkemail(){
    email=$("#email").val();
    var reg = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+((\.[a-zA-Z0-9_-]{2,3}){1,2})$/;
    if(email==""){
      $('div#checkemail').html("<span style=\"color:white\">Email can't be empty</span>");
    }else  if(!reg.test(email)){
      $('div#checkemail').html("<span style=\"color:white\">Bad email form!</span>");
      email = null;
    }else{
      $('div#checkemail').html("<span style=\"color:white\">Right email form</span>");
    }
  }

  function reg_checkpasswd(){
    password=$("#password").val();
    if(password=="" || password.length<6){
      $('div#checkpasswd').html("<span style=\"color:white\">password is 6 digit number!</span>");
    }else{
      $('div#checkpasswd').html("<span style=\"color:white\">enter is ok</span>");
    }
  }

  function reg_checkpasswd2(){
    var toLoad = $(this).attr('href');  
    password2=$("#password2").val();
    if(password2 != password){
      $('div#checkpasswd2').html("<span style=\"color:white\">Different with enter before </span>");
    }
    else{
      $('div#checkpasswd2').html("<span style=\"color:white\">Right! </span>");
    }
  }
    function reg_verify(){
    uname=$("#name").val();
    email=$("#email").val();
    password2=$("#password2").val();
    load = $(this).attr("href");
    if (email=="") { 
      alert("email can't be empty!" );
    }else if(password2 != password){
        $('div#checkpasswd2').html("<span style=\"color:white\">Different with enter before </span>");
      }
    else{
      $('div#checkpasswd2').html("<span style=\"color:white\">Right! </span>");
      var r = confirm("Will your regiser?");
      if (r==true){
          $.getJSON("/ajax/user_register", {"uname":uname,"email":email,"password":password}, function(data){
            if(data == null){
              alert("Email already exist,regiser faild!");
            }else if(data==0){
              alert("Regiser sucess! Begin you tour......");
              window.location.href="index";
              }else{
                alert("Register faild ,check your network!");
              }
            });
        }else{
          window.location.href="regiser";
        }
    }
  }
// index.htm js code 
   function in_checkemail(){
    email=$("#email").val();
    if(email==""){
      $('div#checkemail').html("<span style=\"color:white\">email can't be empty</span>");
    }
  }
  function in_verify(){
    password=$("#password").val();
    if(password=="" || password.length<6){
      $('div#checkpasswd').html("<span style=\"color:white\">password is 6 digit number!</span>");
    }else{
      //$('div#checkpasswd').html("<span style=\"color:white\">enter is ok</span>");
       $.getJSON("/ajax/user_login", {"email":email,"password":password}, function(data){
        if(data == 0){
          var r = confirm("Wil you login?");
          if (r==true){
          alert("Welcome!");
          window.location="Dashboard";
        // $('div#checkpasswd').html("<span style=\"color:white\">password is wrong!</span>");  
          }else{
            window.location="/";
          }
        }
        else{
          alert("Wrong password!");
          window.location="/";
        }
        });
    }
  }
//retrieve.html js code
   function re_checkemail(){
    email=$("#email").val();
    if(email==""){
      $('div#checkemail').html("<span style=\"color:white\">email can't be empty</span>");
    }
  }

  function re_checkpasswd(){
    password=$("#password").val();
    if(password=="" || password.length<6){
      $('div#checkpasswd').html("<span style=\"color:white\">password is 6 digit number!</span>");
    }else{
      $('div#checkpasswd').html("<span style=\"color:white\">enter is ok</span>");
    }
  }

  function re_checkpasswd2(){
    var toLoad = $(this).attr('href');  
    password2=$("#password2").val();
    if(password2 != password){
      $('div#checkpasswd2').html("<span style=\"color:white\">Different with enter before </span>");
    }
    else{
      $('div#checkpasswd2').html("<span style=\"color:white\">Right! </span>");
    }
  }
    function re_verify(){
    password2=$("#password2").val();
    load = $(this).attr("href");
    if(password2 != password){
      $('div#checkpasswd2').html("<span style=\"color:white\">Different with enter before </span>");
    }
    else{
      $('div#checkpasswd2').html("<span style=\"color:white\">Right! </span>");
      $.getJSON("/ajax/user_register/", {"email":email,"password":password}, function(data){
        if(data["result"] == 1){
          alert("Regiser faild!");
        }else{
          alert("Regiser sucess! Begin you tour......");
          window.location.href="index";
        }
        });
    }
  }

// userboard js code
function user_checkname(){
      name=$("#name").val();
      if(name==""){
        $('div#checkname').html("<span style=\"color:white\">Name can't be empty</span>");
      }else{
        $('div#checkname').html("<span style=\"color:white\">Correct name form</span>");
      }
  }


  function user_checkpasswd(id){
    if(id=="old"){    
      oldpwd=$("#old").val();
      $.getJSON("ajax/user_old_passwd",{"password":oldpwd},function(data){
        if(data==0){
          $('div#oldcheck').html("<span style=\"color:white\">Correct password</span>");
      }else{
          $('div#oldcheck').html("<span style=\"color:white\">Wrong password</span>");
          }
        });
    }
    else if(id=="new"){
        newpwd=$("#new").val();
        if(newpwd=="" || newpwd.length<6 ){
          $('div#newcheck').html("<span style=\"color:white\">Wrong form</span>");
        }else if (newpwd==oldpwd){
          $('div#newcheck').html("<span style=\"color:white\">New password can't be same with the old one!</span>");
        }
        else{
          $("div#newcheck").html("<span style=\"color:white\">Correct form</span>");
        }
      }
    else if(id=="again"){
      newpwd2=$("#again").val();
      if(newpwd2 != newpwd){
        $('div#checkpasswd2').html("<span style=\"color:white\">Different with enter before</span>");}
      else{
          $('div#checkpasswd2').html("<span style=\"color:white\">Right </span>");
        }
     }
  }

    function user_verify(){
    password2=$("#new").val();
    password=$("#again").val();
    name=$("#name").val();
    if(password2 != password){
      $('div#checkpasswd2').html("<span style=\"color:white\">Different with enter before </span>");
    }
    else{
      $('div#checkpasswd2').html("<span style=\"color:white\">Right! </span>");
          var r=confirm("Will you reset?");
          if(r==true){
          $.getJSON("ajax/user_passwd_change",{"name":name,"password":password2},function(data){
            if(data==1){
              alert("New information saved!");
              window.location="Dashboard";
            }else{
              alert("New information saved faild!");
              window.location="userboard";
              }
        });
        }else{
          window.location="Dashboard";
        }
    }
  }
  
  function logout(){
    var r=confirm("Will you logout?");
    if (r==true){
      $.getJSON("/ajax/user_logout",{},function(result){
        if (result==0) 
          alert("Logout sucess");
        window.location="/"
      });
    }
}