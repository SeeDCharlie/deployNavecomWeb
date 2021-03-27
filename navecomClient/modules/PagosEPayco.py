from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
import json
from django.shortcuts import redirect
from ..models import *
from django.conf import settings
import requests

class PagosEPayco():
        
    def checkPlanToPay(self, request):
        try:
            idPlan = int(json.loads(request.POST.get('dats'))['idPlan'])
            query = plan.objects.filter(pk= idPlan)
            if query.exists() :
                pln = query.get(pk=idPlan)
                print("id plan : " , pln.id_plan )
                if pln.estado_plan == estados_plan.objects.get(pk=4) or pln.estado_plan == estados_plan.objects.get(pk=2) :
                    return JsonResponse({'success': True, 'url': reverse( 'preFactura', kwargs={'idPlan' : pln.id_plan } ) })
                else :
                    return JsonResponse({'success': False, 'msj': 'No tienes saldo por pagar'})
            else:
                return JsonResponse({'success': False, 'msj': 'El plan que ingreso no existe en nuesta base de datos'})
        except Exception as error:
            print(error)
            return JsonResponse({'success': False, 'msj': 'No pudimos procesar tu solicitud\nVerifica el numero que ingresaste o intenta mas tarde'})
    
    def sendDatsCleintToPay(self, request):
        try:
            idFact = int(json.loads(request.POST.get('dats'))['id_fact'])
            query = facturas.objects.filter(pk= idFact)
            if query.exists() :
                fact = query.get(pk=idFact)
                billing = fact.plan.contrato.cliente
                #key, amount, name, description, price, document 
                if not fact.pago :
                    dats = {
                        'key': settings.PUBLIC_KEY, 
                        'name': 'Plan de Internet' , 
                        'description':( fact.plan.servicio.servicio.nombre_servicio + " " + fact.plan.servicio.complemento_servicio),
                        'id_fact': fact.id_bill ,
                        'price' : fact.total_pagar,
                        'name_billing': (billing.nombre + " " + billing.apellido),
                        'address' : billing.direccion,
                        'document': billing.no_documento,
                        'phone': billing.no_celular
                            
                            }
                    return JsonResponse({'success': True, 'dats': dats})
                else:
                    return JsonResponse({'success': False, 'msj': 'La factura ya fue cancelada, gracias por su fidelidad'})
            else:
                return JsonResponse({'success': False, 'msj': 'El plan que ingreso no existe en nuesta base de datos'})
        except Exception as error:
            print("error : ", error)
            return JsonResponse({'success': False, 'msj': 'No pudimos procesar tu solicitud\nVerifica el numero que ingresaste o intenta mas tarde'})