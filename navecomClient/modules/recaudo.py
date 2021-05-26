from ..models import *
from datetime import datetime, timedelta 

class Recaudo():


    def generarFacturas(self, diaPago):
        plns = plan.objects.all().filter(
            dia_inicio_pago = diaPago,
            estado_plan__id_state_plan = 1)
        for pln in plns:
            newFact = self.generarFacturaPlan(pln)
            self.agregarMontosFactura(self.getMontosPlan(pln), newFact )
            self.agregarDescuentosFactura(self.getDescuentosPlan(pln), newFact)
            newFact.total_pagar = self.calcularMontoTotal(newFact) - self.calcularDescuentoTotal(newFact)
            newFact.save(update_fields=['total_pagar'], force_update=True)

#sacar todos los montos y descuentos de los planes, agragarlos a la nueva factura, restarles un
#dia de mes al que aplican y hacer el calculo total de la factura

    def getMontosPlan(self, plan):
        return montos_plan.objects.all().filter(plan = plan, estado = 'p')
    
    def getDescuentosPlan(self, plan):
        return descuentos_plan.objects.all().filter(plan = plan, estado = 'p')
    
    def generarFacturaPlan(self, plan):
        fullDate = datetime.now() + timedelta(days=5)
        nuevaFactura = facturas(plan = plan, fecha_limite_pago = fullDate)
        nuevaFactura.save()
        return nuevaFactura
    
    def agregarMontosFactura(self, listaMontos, factura):
        for monto in listaMontos:
            monto.factura = factura
            monto.no_meses_aplica = monto.no_meses_aplica - 1
            if monto.no_meses_aplica == 0:
                monto.estado = 'c'
            monto.save(update_fields=['factura'], force_update=True)

    def agregarDescuentosFactura(self, listaDescuentos, factura):
        for descuento in listaDescuentos:
            descuento.factura = factura
            descuento.no_meses_aplica = descuento.no_meses_aplica - 1
            if descuento.no_meses_aplica == 0:
                descuento.estado = 'c'
            descuento.save(update_fields=['factura'], force_update=True)
    
    def calcularMontoTotal(self, factura):
        return montos_plan.objects.filter(factura = factura).annotate(sum('monto_adicional__precio'))

    def calcularDescuentoTotal(self, factura):
        return descuentos_plan.objects.filter(factura = factura).annotate(sum('descuentos__precio'))
