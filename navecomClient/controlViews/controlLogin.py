from ..modules.manageUsers.managUsr import ManagUsr
from django.http import  JsonResponse
from django.urls import reverse

class ControlLogin():

    def __init__(self):
        self.ctrl = ManagUsr()

    def loggin(self,request,  email, passw ):
        rLogin = self.ctrl.loggin(request, email, passw)
        if rLogin:
            #str(reverse('index'))
            return JsonResponse({'msj': "usuario : %s , contraseña: %s"%(email, passw), 'url': reverse('factClient'), 'log': True,'success': True})

        else:
            return JsonResponse({'msj': 'usuario o contraseña incorrectos', 'success': False})

    def logOut(self, request):
        return self.ctrl.logOut(request)