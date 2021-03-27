from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template, render_to_string
from easy_pdf.rendering import render_to_pdf_response
from django.urls import reverse
import json
from django.shortcuts import redirect
from .controlViews.controlLogin import ControlLogin
from .models import *
from django.conf import settings
import hashlib
import requests

# Create your views here.


# metodos para la devolucion de vistas html
def not_found_404(request,exception=None):
    return render(request,'navecomClient/error_404.html')

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

## Esta funcion checkea el estado de un plan. si el plan tienen facturas por pagar se retornara una url que redirigira al suaurio a una
## pagina con el resumen de la factura que debe pagar
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



## funcion que retorna los datos de la factura que debe ir incluidos en la peticion de pago a epayco 
## data-epayco-costo, data-epayco-cliente, data-epayco-descripcion etc

def getDatsForEpayco(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and request.method == 'POST':
        try:
            idFact = int(json.loads(request.POST.get('dats'))['id_fact'])
            query = facturas.objects.filter(pk= idFact)
            if query.exists() :
                fact = query.get(pk=idFact)
                billing = fact.plan.contrato.cliente
                #key, amount, name, description, price, document 
                if not fact.pago :
                    dats = {'key': settings.PUBLIC_KEY, 'name': 'Plan de Internet' , 'description':( fact.plan.servicio.servicio.nombre_servicio + " " + fact.plan.servicio.complemento_servicio ),
                            'id_fact': str(fact.id_bill) , 'price' : str(fact.total_pagar), 'name_billing': (billing.nombre + " " + billing.apellido), 'address' : billing.direccion,
                            'document': str(billing.no_documento), 'phone':str(billing.no_celular)}
                    return JsonResponse({'success': True, 'dats': dats})
                else:
                    return JsonResponse({'success': False, 'msj': 'La factura ya fue cancelada, gracias por su fidelidad'})
            else:
                return JsonResponse({'success': False, 'msj': 'El plan que ingreso no existe en nuesta base de datos'})
        except Exception as error:
            print("error : ", error)
            return JsonResponse({'success': False, 'msj': 'No pudimos procesar tu solicitud\nVerifica el numero que ingresaste o intenta mas tarde'})
    return redirect('index')


def responseTransactionEpayco(request):
    
    if request.method == 'GET' :
        context = {'msj': 'no se encontro referencia de pago'}
        try :
            urlapp = "https://secure.epayco.co/validation/v1/reference/" + str(request.GET.get('ref_payco'))
            response = requests.get(urlapp)
    
            if response :
                response = response.json()['data']
                context = {'fecha': response.x_transaction_date,
                            'respuesta':response.x_response ,
                            'referencia': response.x_id_invoice,
                            'motivo': response.x_response_reason_text,
                            'recibo': response.x_transaction_id,
                            'banco': response.x_bank_name,
                            'autorizacion': response.x_approval_code,
                            'total':(response.x_amount + ' ' + response.x_currency_code),
                            'msj':''
                            }
                if response.x_cod_response == 1:
                #Codigo personalizado
                    context.msj = "Transaccion Aprobada"          
                #Transaccion Rechazada
                if response.x_cod_response == 2:
                    context.msj = 'transacción rechazada'

                #Transaccion Pendiente
                if response.x_cod_response == 3:
                    context.msj = 'transacción pendiente'

                #Transaccion Fallida
                if response.x_cod_response == 4:
                    context.msj = 'transacción fallida'

                return render(request, 'navecomClient/responseTransactionEpayco.html', context)
        except Exception as error : 
            return render(request, 'navecomClient/responseTransactionEpayco.html', context)
    else :
        return redirect('solicitud')

## metodo que recibe los datos y estado de la transaccion por part de epayco estos datos son enviados por POST metodo
##

def confirmationTransactionEpayco(request):
    
    if request.method == 'POST':

        x_ref_payco      = request.POST.get('x_ref_payco')
        x_transaction_id = request.POST.get('x_transaction_id')
        x_amount         = request.POST.get('x_amount')
        x_currency_code  = request.POST.get('x_currency_code')
        x_signature      = request.POST.get('x_signature')

        signature = hashlib.sha256()
        signature.update(settings.P_CUST_ID_CLIENTE + '^' + settings.P_KEY + '^' + x_ref_payco + '^' + x_transaction_id + '^' + x_amount + '^' + x_currency_code)

        x_response     = request.POST.get('x_response')
        x_motivo       = request.POST.get('x_response_reason_text')
        x_id_invoice   = request.POST.get('x_id_invoice')
        x_autorizacion = request.POST.get('x_approval_code')

        id_fact = request.POST.get('x_id_factura')       
        #Validamos la firma
        if x_signature == signature.digest() :
            if x_cod_response == 1 :
                print("transaccion aceptada : ", id_fact)
            if x_cod_response == 2 :
                print("transaccion rechazada : ", id_fact)
            if x_cod_response == 3 :
                print("transaccion pendiente", id_fact)
            if x_cod_response == 4 :
                print("transaccion fallida", id_fact)

        else:
            print('Firma no valida')

        return redirect('index')
    else :
        return redirect('index')