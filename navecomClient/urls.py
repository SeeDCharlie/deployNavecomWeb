from django.urls import path,re_path

from .views import *



urlpatterns = [
    path('pruebas/<int:idPlan>',pruebas, name = 'pruebas'),

    path( '', index, name = 'index'),
    path( 'prueba/' , prueba  , name = 'prueba'),
    path( 'login/', login, name = 'login'),
    path( 'logOut/', logOut, name = 'logOut'),
    path( 'solicitud/', solicitud, name = 'solicitud'),
    path( 'factClient/', factClient , name = 'factClient'),
    path( 'logUsr/' , loginUsr  , name = 'logUsr'),
    path( 'getDataContact/' , getDataContact  , name = 'getDataContact'),
    path( 'pagos/' , pagos  , name = 'pagos'),
    path( 'preFactura/<int:idPlan>/' , preFactura  , name = 'preFactura'),
    path( 'downloadFact/<int:id_fact>/' , downloadFact , name='downloadFact'),
    path( 'checkFacturaPlan/', checkFacturaPlan, name="checkFacturaPlan" ),
    path( 'getDatsForEpayco/' , getDatsForEpayco, name='getDatsForEpayco'),

    path( 'responseTransactionEpayco/', responseTransactionEpayco, name='responseTransactionEpayco'),
    path( 'confirmationTransactionEpayco/', confirmationTransactionEpayco, name='confirmationTransactionEpayco'),

    path( 'resposeGeneratePIN/', respuestaGenerarPIN, name='respuestaGenerarPIN'),
    path( 'confirmTransactionPINEpayco/', confirmacionTransaccionPagoPorPIN, name='confirmacionTransaccionPagoPorPIN'),


]
