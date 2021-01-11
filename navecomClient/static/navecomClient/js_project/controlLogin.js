// eventos de botones


//btn loggin action
$('#btnLoggin').on("click", function(){

    var email = $('#inputEmailLoggin').val() ;
    var pass = $('#inputPasswordLoggin').val();
    var datos = JSON.stringify({
        email: email,
        pass: pass,
    });

    requestAjax('btnLoggin', datos);
    

});


function respuestaAjax(data){
    window.location.replace(data.url);

}
