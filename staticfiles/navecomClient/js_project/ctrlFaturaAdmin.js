


window.addEventListener("load", function() {

    function respuestaAjax(data){
        alert("respuesta ajax" + data.msj);
    }
    
    function errorSucces(msj){
        alert("error ajax : " + msj  );
    }


    (function($) {

        function requestAjax(btnName, datos) {
            $.ajax({
                url: $('#' + btnName).attr('url'),
                data: {
                    dats: datos,
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                    action: 'post'
                },
                type: 'POST',
                dataType: 'json',
                success: function (data) {
                    if (data.success) {
                        respuestaAjax(data);
                    }
                    else {
                        errorSucces(data.msj);
                    }
                },
                error: function () {
                    errorAjax();
                }
            });
        }


        $(document).on('click','.downloadFact', function(){

            var id_fact =  $(this).attr('id_fact');

            var datos = JSON.stringify({
                id_fact: id_fact,
            });       

        });
    })(django.jQuery);
});





