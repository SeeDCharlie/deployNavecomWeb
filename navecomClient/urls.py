from django.urls import path,re_path


from .views import *

urlpatterns = [
    path( '', index, name = 'index'),
    path( 'prueba/' , prueba  , name = 'prueba'),
    path( 'login/', login, name = 'login'),
    path( 'logOut/', logOut, name = 'logOut'),
    path( 'solicitud/', solicitud, name = 'solicitud'),
    path( 'homeClient/', homeClient , name = 'homeClient'),
    path( 'logUsr/' , loginUsr  , name = 'logUsr'),
    path( 'getDataContact/' , getDataContact  , name = 'getDataContact'),
    path( 'pagos/' , pagos  , name = 'pagos'),
    path( 'preFactura/<int:idPlan>/' , preFactura  , name = 'preFactura'),
    path( 'downloadFact/<int:id_fact>/' , downloadFact , name='downloadFact'),
    path( 'checkFacturaPlan/', checkFacturaPlan, name="checkFacturaPlan" ),
    path( 'getDatsForEpayco/' , getDatsForEpayco, name='getDatsForEpayco'),
    re_path( r'^responseTransactionEpayco/(?P<ref_payco>/\w+)/$', responseTransactionEpayco, name='responseTransactionEpayco'),
    path( 'confirmationTransactionEpayco/', confirmationTransactionEpayco, name='confirmationTransactionEpayco'),
]
