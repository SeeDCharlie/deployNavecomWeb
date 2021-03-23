window.addEventListener('scroll', function(){
    if ($(this).scrollTop() > 1) {
       $('.topnav').attr('style',"background-color: rgba(255, 255, 255, 1) !important;" );
       $('.topnav .itemMenuBar').attr("style", "color: rgb(175, 175, 175 ) ; ");

     } 
     if($(this).scrollTop() == 0)  {
        $('.topnav').attr('style',"background-color: rgba(255, 255, 255, 0) !important;" );
        $('.topnav .itemMenuBar').attr("style", "color: rgb(175, 175, 175 ) ; ");
     } 

}, true);




function showToastMsj(title, msj, color = "#00425C"){
  $('.titleToast').text(title);
  $('.bodyToast').text(msj);

  $('.bodyTo').css("background-color", color);

  var x = document.getElementById("toastMsj");
  x.className = "show";
  setTimeout(function(){ x.className = x.className.replace("show", ""); }, 5000);

}
