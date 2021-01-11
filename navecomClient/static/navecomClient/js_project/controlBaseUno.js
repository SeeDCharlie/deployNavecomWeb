window.addEventListener('scroll', function(){
    if ($(this).scrollTop() > 1) {
       $('.mainMenuOne').attr('style',"background-color: rgba(255, 255, 255, 1) !important;" );
       $('.textMenu').attr("style", "color: rgb(175, 175, 175 ) ; ");

     } 
     if($(this).scrollTop() == 0)  {
        $('.mainMenuOne').attr('style',"background-color: rgba(255, 255, 255, 0) !important;" );
        $('.textMenu').attr("style", "color: rgb(255, 255, 255 ) ; ");
     } 

}, true);