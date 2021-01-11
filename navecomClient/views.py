from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from django.shortcuts import redirect
from .controlViews.controlLogin import ControlLogin
# Create your views here.


# metodos para la devolucion de vistas html
def not_found_404(request,exception=None):
    return render(request,'navecomClient/error_404.html')

def index(request):
    return render(request,'navecomClient/index.html')

def login(request):
    return render(request,'navecomClient/login.html')

def solicitud(request):
    return render(request,'navecomClient/solicitud.html')

def homeClient(request):

    if request.user.is_authenticated : 
        return render(request, 'navecomClient/templatesClient/homeClient.html')
    else:
        return redirect('index')

# metodos de funcionalidades

def loginUsr(request):

    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        c = ControlLogin()
        email = json.loads(request.POST.get('dats'))['email']
        passw = json.loads(request.POST.get('dats'))['pass']

        print("email : " , email, "   passw : " , passw )

        return c.loggin(request, email, passw)
        
    else :
        return login(request)


def logOut(request):
    c = ControlLogin()
    c.logOut(request)
    return redirect('index')
 