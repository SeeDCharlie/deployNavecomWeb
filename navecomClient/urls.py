from django.urls import path


from .views import *

urlpatterns = [
    path('', index, name = 'index'),
    path('login/', login, name = 'login'),
    path('logOut/', logOut, name = 'logOut'),
    path('solicitud/', solicitud, name = 'solicitud'),
    path('homeClient/', homeClient , name = 'homeClient'),
    path( 'logUsr/' , loginUsr  , name = 'logUsr'),
]

handler404 = 'navecomClient.views.not_found_404'
