window.addEventListener('scroll', function(){
    if ($(this).scrollTop() > 1) {
       $('.topnav').attr('style',"background-color: rgba(255, 255, 255, 1) !important;" );
       $('.itemMenuBar').attr("style", "color: rgb(175, 175, 175 ) ; ");

     } 
     if($(this).scrollTop() == 0)  {
        $('.topnav').attr('style',"background-color: rgba(255, 255, 255, 0) !important;" );
        $('.itemMenuBar').attr("style", "color: rgb(175, 175, 175 ) ; ");
     } 

}, true);


function myFunction() {
   var x = document.getElementById("myTopnav");
   if (x.className === "topnav fixed-top") {
     x.className += " responsive";
   } else {
     x.className = "topnav fixed-top";
   }
 }