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
            query = plan.objects.filter(pk=idPlan)
            if query.exists():
                pln = query.get(pk=idPlan)
                print("id plan : ", pln.id_plan)
                if pln.estado_plan == estados_plan.objects.get(pk=4) or pln.estado_plan == estados_plan.objects.get(pk=2):
                    return JsonResponse({'success': True, 'url': reverse('preFactura', kwargs={'idPlan': pln.id_plan})})
                else:
                    return JsonResponse({'success': False, 'msj': 'No tienes saldo por pagar'})
            else:
                return JsonResponse({'success': False, 'msj': 'El plan que ingreso no existe en nuesta base de datos'})
        except Exception as error:
            print(error)
            return JsonResponse({'success': False, 'msj': 'No pudimos procesar tu solicitud\nVerifica el numero que ingresaste o intenta mas tarde'})

    def sendDatsCleintToPay(self, request):
        try:
            idFact = int(json.loads(request.POST.get('dats'))['id_fact'])
            query = facturas.objects.filter(pk=idFact)
            if query.exists():
                fact = query.get(pk=idFact)
                billing = fact.plan.contrato.cliente
                #key, amount, name, description, price, document
                if not fact.pago:
                    dats = {
                        'key': settings.PUBLIC_KEY,
                        'name': 'Plan de Internet',
                        'description': (fact.plan.servicio.servicio.nombre_servicio + " " + fact.plan.servicio.complemento_servicio),
                        'id_fact': fact.id_bill,
                        'price': fact.total_pagar,
                        'name_billing': (billing.nombre + " " + billing.apellido),
                        'address': billing.direccion,
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

    def checkResponseTransactionPayco(self, request):
        try :
            x_ref_payco      = request.POST.get('x_ref_payco')
            x_transaction_id = request.POST.get('x_transaction_id')
            x_amount         = request.POST.get('x_amount')
            x_currency_code  = request.POST.get('x_currency_code')
            x_signature      = request.POST.get('x_signature')

            signature = hashlib.sha256()
            signature.update(str(settings.P_CUST_ID_CLIENTE) + '^' + str(settings.P_KEY) + '^' + 
                        str(x_ref_payco) + '^' + str(x_transaction_id) + '^' + str(x_amount) + '^' + str(x_currency_code))

            x_response     = request.POST.get('x_response')
            x_motivo       = request.POST.get('x_response_reason_text')
            x_id_invoice   = request.POST.get('x_id_invoice')
            x_autorizacion = request.POST.get('x_approval_code')
            x_type_payment = request.POST.get('x_type_payment')
            x_transaction_date = requests.POST.get('x_transaction_date')

            id_fact = request.POST.get('x_id_factura')       
            #Validamos la firma
            if x_signature == signature.digest() :
                if x_cod_response == 1 :
                    self.transactionConfirmPayco(x_type_payment,x_ref_payco,x_autorizacion, x_transaction_id,x_transaction_date, id_fact)
                if x_cod_response == 2 :
                    print("transaccion rechazada : ", id_fact)
                if x_cod_response == 3 :
                    print("transaccion pendiente", id_fact)
                if x_cod_response == 4 :
                    print("transaccion fallida", id_fact)

            else:
                print('Firma no valida')

        except Exception as error:
            print('error : ', error)

    def transactionConfirmPayco(self, *args):
        fact = facturas.objects.get(pk=args[5])
        fact.pago = 1
        fact.type_method = args[0]
        fact.referencia_payco = args[1]
        fact.codigo_aprobacion_payco = args[2]
        fact.numero_recibo_transaccion = args[3]
        fact.fecha_pago = args[4]
        id_plan = fact.plan.id_plan
        fact.save(update_fields=['pago','type_method',
                        'referencia_payco',
                        'codigo_aprobacion_payco',
                        'numero_recibo_transaccion',
                        'fecha_pago'], force_update=True)
        if self.checStatePlanOk(id_plan):
            pln = Plan.objects.get(pk=id_plan)
            pln.estado_plan = estados_plan.objects.get(pk=1)
            pln.save(update_fields=['estado_plan'], force_update=True)

        print("transaccion aceptada : ", args[4])

    def checStatePlanOk(self, id_plan):
        plan = Plan.objects.get(pk=id_plan)
        query = facturas.objects.filter(plan=plan)
        if query.exists():
            return True
        else:
            return False
        
