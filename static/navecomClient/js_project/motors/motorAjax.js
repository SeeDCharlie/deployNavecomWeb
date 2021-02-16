function requestAjax(btnName,datos){
    $.ajax({
        url: $('#'+btnName).attr('url'),
        data: {
            dats:datos,
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

