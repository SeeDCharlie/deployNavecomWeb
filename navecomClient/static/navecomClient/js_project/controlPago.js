// eventos de botones

//btn send idPlan
$('#btnPlan').on("click", function(){
    var idPlan = $('#idPlan').val() ;    
    var datos = JSON.stringify({
        idPlan: idPlan,        
    });
    requestAjax('btnPlan', datos);
});

function respuestaAjax(data){
    window.location.replace(data.url);
}

function errorSucces(msj){
    showToastMsj('Error !', msj, "#E63120");
}
