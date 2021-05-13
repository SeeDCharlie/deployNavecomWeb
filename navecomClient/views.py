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
from .modules.PagosEPayco import PagosEPayco
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


# metodos para la devolucion de vistas html
def not_found_404(request,exception=None):
    return render(request,'navecomClient/error_404.html')

def index(request):
    return render(request,'navecomClient/index.html')

def pagos(request):
    return render(request,'navecomClient/pago.html')    

def prueba(request):
    return render(request,'navecomClient/prueba.html')

def login(request):
    return render(request,'navecomClient/login.html')

def solicitud(request):
    context = {'planes':categorias_servicio.objects.all()}
    return render(request,'navecomClient/solicitud.html', context)

def logOut(request):
    ControlLogin().logOut(request)
    return redirect('index')

# login
def loginUsr(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and request.method == 'POST':
        c = ControlLogin()
        email = json.loads(request.POST.get('dats'))['email']
        passw = json.loads(request.POST.get('dats'))['pass']
        return c.loggin(request, email, passw)
    else :
        return redirect('login')

def factClient(request):
    if request.user.is_authenticated : 
        return render(request, 'navecomClient/factClient.html')
    else:
        return redirect('index')

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
                return render(request, 'navecomClient/preFactura.html' ,{'error': True, 'msj': 'USTED NO TIENE SALDO PENDIENTE POR PAGAR' })
        except Exception as error:
            print(error)
            return render(request, 'navecomClient/preFactura.html', {'error': True, 'msj': 'LO SENTIMOS, POR FAVOR INTENTE MAS TARDE.' })
  

# metodos de funcionalidades

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
        pagosMod = PagosEPayco()
        return pagosMod.checkPlanToPay(request)
    return redirect('index')

## funcion que retorna los datos de la factura que debe ir incluidos en la peticion de pago a epayco 
## data-epayco-costo, data-epayco-cliente, data-epayco-descripcion etc

def getDatsForEpayco(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and request.method == 'POST':
        pagosMod = PagosEPayco()
        return pagosMod.sendDatsCleintToPay(request)
    return redirect('index')

def responseTransactionEpayco(request):
    
    if request.method == 'GET' :
        context = {'msj': 'no se encontro referencia de pago'}
        try :
            urlapp = "https://secure.epayco.co/validation/v1/reference/" + str(request.GET.get('ref_payco'))
            response = requests.get(urlapp)
            if response :
                response = response.json()['data']
                fact = facturas.objects.get(pk=response['x_id_invoice'])
                context = {
                    'fecha': response['x_transaction_date'],
                    'referenciaPayco': response['x_ref_payco'],
                    'no_factura': response['x_id_invoice'],
                    'motivo': response['x_description'],
                    'recibo': response['x_transaction_id'],
                    'banco': response['x_bank_name'],
                    'total':( str(response['x_amount']) + ' ' + str(response['x_currency_code']) ),
                    'estado_transaccion' : response['x_transaction_state'],
                    'payment_type':response['x_type_payment'],
                    'fact':fact,
                    'msj':''
                        }
                #Transaccion Aprobada
                if response['x_cod_response'] == 1:
                    context['msj'] = "Transaccion Aprobada"  
                #Transaccion Rechazada
                if response['x_cod_response'] == 2:
                    context['msj'] = 'transacción rechazada' 
                #Transaccion Pendiente
                if response['x_cod_response'] == 3:
                    context['msj'] = 'transacción pendiente' 
                #Transaccion Fallida
                if response['x_cod_response'] == 4:
                    context['msj'] = 'transacción fallida'
                return render(request, 'navecomClient/responseTransactionEpayco.html', context)
            else:
                context['error'] = True
                context['msj'] = "Lo sentimos, intente mas tarde, si el problema persiste comuniquese con nosotros"
                return render(request, 'navecomClient/responseTransactionEpayco.html', context)
        except Exception as error : 
            context['error'] = True
            context['msj'] = "Lo sentimos, intente mas tarde, si el problema persiste comuniquese con nosotros.\n error:" + str(error) 
            return render(request, 'navecomClient/responseTransactionEpayco.html', context)
    else :
        return redirect('solicitud')

## metodo que recibe los datos y estado de la transaccion por part de epayco estos datos son enviados por POST metodo
##
@csrf_exempt
def confirmationTransactionEpayco(request):
    if request.method == 'POST':
        try:
            pagosMod = PagosEPayco()
            print("request content : ",[ str(i) for i in request.POST.items()] )
            return pagosMod.checkResponseTransactionPayco(request)
        except Exception as error:
            return JsonResponse({'success': False, 'msj':'error 1.2 : %s'%str(error)})
    else :
        return redirect('index')

def respuestaGenerarPIN(request):
    if request.method == 'POST':
        print("respuesta transaction PIN: ", [ str(i) for i in request.GET.items()])
        return JsonResponse({"respuesta(generar PIN)": [ str(i) for i in request.POST.items()]})
    else :
        return redirect('index')
        
@csrf_exempt
def confirmacionTransaccionPagoPorPIN(request):

    if request.method == 'POST':
        try:
            dats = request.body
            if request.POST.get('success'):
                data = request.POST.get('data')
                if data['x_cod_response'] == 1:
                    fact = facturas.objects.get(pk=int(data['x_id_factura']))
                    fact.pago = 1
                    fact.fecha_pago = data['x_transaction_date']
                    fact.referencia_payco = data['x_ref_payco']
                    fact.type_method = data['x_bank_name']
                    fact.codigo_aprobacion_payco = data['x_approval_code']
                    fact.numero_recibo_transaccion = data['x_transaction_id']
                    fact.save(update_fields=['fecha_pago','referencia_payco',
                                            'type_method','codigo_aprobacion_payco','numero_recibo_transaccion'], force_update=True)
                    pln = fact.plan
                    pln.estado_plan = estados_plan.objects.get(pk=1)
                    pln.save(update_fields=['estado_plan'], force_update=True)
                    return JsonResponse({"ok": True})
                else:
                    log = logsnavecomsystem(log_name="error confirmacionTransaccionPagoPorPIN", log_description="aun no se ha hecho el pago fisico")
                    log.save()
                    return JsonResponse({"error confirmacionTransaccionPagoPorPIN": str(dats)})
            else:
                log = logsnavecomsystem(log_name="error confirmacionTransaccionPagoPorPIN", log_description=str(dats))
                log.save()
                return JsonResponse({"error confirmacionTransaccionPagoPorPIN": str(dats)})
        except Exception as error:
            log = logsnavecomsystem(log_name="error inesperado confirmacionTransaccionPagoPorPIN", log_description=str(error))
            log.save()
            return JsonResponse({"error inesperado confirmacionTransaccionPagoPorPIN": str(error)})
    else :
        return redirect('index')


def pruebas(request, idPlan):
    p = PagosEPayco()
    fact = facturas.objects.get(pk=idPlan)
    return JsonResponse( {'respuesta':p.generarPINpagoFisico(fact)})