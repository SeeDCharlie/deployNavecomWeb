$( document ).ready(function() {
    
    function togglePopup() {
        document.getElementById("popupData").classList.toggle("active");
    }

    $('#btnContact').on('click', function(){

        var name = $('#nameSoli').val() ;
        var cell = $('#cellSoli').val();
        var tel = $('#telSoli').val();
        var email = $('#emailSoli').val();
        var dir = $('#dirSoli').val();
        var plan = $('#planSoli').val();
    
        if(name == '' || cell == '' ){
    
            showToastMsj('Error', 'Llene los campos obligatorios.');
    
        }else{
            if (tel == ''){
                tel = null;
            }
            var datos = JSON.stringify({
                name,name,
                cell: cell,
                tel: tel,
                email: email,
                dir: dir,
                plan: parseInt(plan)
            });
            requestAjax('btnContact', datos);
        }
        
    });
    
    
    function respuestaAjax(data){
        showToastMsj('Solicitud enviada!',data.msj);
    }
    
    function errorSucces(msj){
        showToastMsj('Error !', msj);
    }
    
    function errorAjax(){
        showToastMsj('Error!', 'Incongruencia en los datos o intentelo mas tarde')
    }
    
});


