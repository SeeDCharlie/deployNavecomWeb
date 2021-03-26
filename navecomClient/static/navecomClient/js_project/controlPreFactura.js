

$('#btnPayInvoice').on('click', function () {

    var id_fact = $('#btnPayInvoice').attr('id_fact');
    var datos = JSON.stringify({
        id_fact: id_fact,
    });

    requestAjax('btnPayInvoice', datos);
});


function respuestaAjax(data) {

    var handler = ePayco.checkout.configure({
        key: data.dats.key,
        test: true
    });

    var daataPay = {
        //Parametros compra (obligatorio)
        name: data.dats.name,
        description: data.dats.description,
        invoice: data.dats.id_fact,
        currency: "cop",
        amount: data.dats.price,
        tax_base: "0",
        tax: "0",
        country: "co",
        lang: "es",

        //Onpage="false" - Standard="true"
        external: "false",

        //Atributos opcionales
        confirmation: "https://navecomingenieria.com/confirmationTransactionEpayco/",
        response: "https://navecomingenieria.com/responseTransactionEpayco/",

        //Atributos cliente
        name_billing: data.dats.name_billing,
        address_billing: data.dats.address,
        type_doc_billing: "cc",
        mobilephone_billing: data.dats.phone,
        number_doc_billing: data.dats.document,
    }

    handler.open(daataPay);
}



function errorSucces(msj) {
    showToastMsj('Error !', msj);
}


function errorAjax() {
    showToastMsj('Error!', 'Compruebe su conexion a internet e intentelo mas tarde o comuniquese con nosotros')
}