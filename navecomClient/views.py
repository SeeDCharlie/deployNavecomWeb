from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from django.shortcuts import redirect
from .controlViews.controlLogin import ControlLogin
from .models import *

# Create your views here.


# metodos para la devolucion de vistas html
def not_found_404(request,exception=None):
    return render(request,'navecomClient/error_404.html')

def index(request):
    return render(request,'navecomClient/index.html')

def prueba(request):
    return render(request,'navecomClient/prueba.html')

def login(request):
    return render(request,'navecomClient/login.html')

def solicitud(request):
    context = {'planes':categorias_servicio.objects.all()}
    return render(request,'navecomClient/solicitud.html', context)

def homeClient(request):
    if request.user.is_authenticated : 
        return render(request, 'navecomClient/templatesClient/homeClient.html')
    else:
        return redirect('index')

# metodos de funcionalidades

# login
def loginUsr(request):

    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and request.method == 'POST':

        c = ControlLogin()
        email = json.loads(request.POST.get('dats'))['email']
        passw = json.loads(request.POST.get('dats'))['pass']

        return c.loggin(request, email, passw)
        
    else :
        return redirect('login')

def logOut(request):
    ControlLogin().logOut(request)
    return redirect('index')

# formulario contacto

def getDataContact(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and request.method == 'POST':
        dats = json.loads(request.POST.get('dats'))
        try:
            peticion = solicitudes_servicio(nombre = dats['name'], no_celular = dats['cell'], tel_fijo = dats['tel'], email = dats['email'], direccion = dats['dir'])
            if dats['plan'] != -1:
                peticion.plan = categorias_servicio.objects.get(pk=dats['plan'])
            peticion.save()
            return JsonResponse({'success': True, 'msj': 'Un asesor se pondra en contacto con usted'})
        except Exception as error : 
            print(error)
            return JsonResponse({'success': False, 'msj': 'No pudimos procesar la solicitus \n error: %s.'%error})

    return redirect('solicitud')
