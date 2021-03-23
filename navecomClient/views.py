from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template, render_to_string
from easy_pdf.rendering import render_to_pdf_response
from django.urls import reverse
import json
from django.shortcuts import redirect
from .controlViews.controlLogin import ControlLogin
from .models import *

# Create your views here.


# metodos para la devolucion de vistas html

def index(request):
    return render(request,'navecomClient/index.html')

def preFactura(request, idPlan = -1):

    if idPlan < 1 :
        return redirect('index')
    else :
        #no plan, no factura, fecha vencimiento, total a pagar, nombres propietario, nombre plan, total
        try:
            factura = facturas.objects.get(plan=plan.objects.get(pk=int(idPlan)))

            if factura.plan.estado_plan == estados_plan.objects.get(pk=4) :
                
                context = {'factura': factura, 'msj': 'Bienvenido'}
                return render(request, 'navecomClient/preFactura.html', context )
            else :
                return render(request, 'navecomClient/preFactura.html' ,{'error': True, 'msj': 'USTED NOT TIENE SALDO PENDIENTE POR PAGAR' })
        except Exception as error:
            print(error)
            return render(request, 'navecomClient/preFactura.html', {'error': True, 'msj': 'LO SENTIMOS, POR FAVOR INTENTE MAS TARDE.' })
  

def pagos(request):
    return render(request,'navecomClient/pago.html')    

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


#devuelve la factura en pdf. la peticion debe ser ajax y post y llevar dentro el id de la factura

def downloadFact(request, id_fact):

    if request.user.is_authenticated and request.user.tipo_usuario == tipo_usuario.objects.all().get(pk=1)  :

        try:
                
            return render_to_pdf_response(request, 'navecomClient/templatesAdmin/modelFact.html', {'content': "pdf prueba"},
                                      download_filename='prueba.pdf', base_url=request.build_absolute_uri())
        except Exception as error : 
            print(error)
            return JsonResponse({'success': False, 'msj': 'No pudimos procesar la solicitus \n error: %s.'%error})

    return redirect('login')


def checkFacturaPlan(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and request.method == 'POST':
        try:
            idPlan = int(json.loads(request.POST.get('dats'))['idPlan'])
            query = plan.objects.filter(pk= idPlan)
            if query.exists() :
                pln = query.get(pk=idPlan)
                print("id plan : " , pln.id_plan )
                if pln.estado_plan == estados_plan.objects.get(pk=4) :
                    return JsonResponse({'success': True, 'url': reverse( 'preFactura', kwargs={'idPlan' : pln.id_plan } ) })
                else :
                    return JsonResponse({'success': False, 'msj': 'No tienes saldo por pagar'})
            else:
                return JsonResponse({'success': False, 'msj': 'El plan que ingreso no existe en nuesta base de datos'})
        except Exception as error:
            print(error)
            return JsonResponse({'success': False, 'msj': 'No pudimos procesar tu solicitud\nVerifica el numero que ingresaste o intenta mas tarde'})
    return redirect('index')