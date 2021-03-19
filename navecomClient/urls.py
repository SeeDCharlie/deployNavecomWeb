from django.urls import path


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

]

