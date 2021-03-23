from django.contrib import admin
from django.contrib.auth.models import Group, PermissionManager
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.urls import reverse
from .models import *
from .forms import *
from django.db.models import F
from django.utils.html import format_html


from django.contrib.admin.widgets import AutocompleteSelect

# Register your models here.


@admin.register(usuario)
class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm
    model = usuario

    list_display = ('email', 'nombre', 'apellido', 'tipo_usuario')
    list_display_links = ('email', 'nombre')
    list_filter = ('estado', 'tipo_usuario')
    fieldsets = (
        (None, {'fields': ('nickname', 'tipo_usuario', 'estado')}),
        ('Informacion personal', {'fields': ('email', 'no_documento', 'nombre', 'apellido',
                                             'no_celular', 'tel_fijo', 'direccion', 'barrio', 'referencia_vivienda', 'password')}),
        ('Permisos', {'fields': ('groups',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'tipo_usuario', 'no_documento', 'nombre', 'apellido', 'no_celular', 'tel_fijo', 'direccion', 'barrio', 'referencia_vivienda', 'estado', 'nickname', 'password1', 'password2'),
        }),
        ('Permisos', {'fields': ('groups', )}),
    )

    #radio_fields = {"estado": admin.VERTICAL}

    search_fields = ('email', 'nombre', 'apellido')
    ordering = ('email', 'estado')
    filter_horizontal = ('groups', )

    readonly_fields = ('estado',)

    def grupos(self, obj):
        return obj.groups.exclude(permission=1)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.tipo_usuario == tipo_usuario.objects.get(pk=1):
            return qs
        return qs.exclude(tipo_usuario=1).exclude(tipo_usuario=2)


@admin.register(categorias_servicio)
class planesServiciosAdmin(admin.ModelAdmin):

    list_display = ('id_cat_ser', 'servicio', 'complemento_servicio', 'costo')
    list_display_links = ('id_cat_ser', 'servicio', 'complemento_servicio')
    list_filter = ('zonas', 'servicio')
    search_fields = ['complemento_servicio',
                     'servicio__nombre_servicio', 'zonas__nombre']
    filter_horizontal = ('zonas', )

    def nombre_zonas(self, obj):
        return ' '.join(name_z.__str__() for name_z in obj.zonas.all())


@admin.register(contrato)
class contratoAdmin(admin.ModelAdmin):

    list_filter = ('activo',)
    list_display = ('id_contract', 'cliente', 'nombre', 'apellido', 'activo')
    list_display_links = ('id_contract', 'cliente')
    autocomplete_fields = ['cliente']
    search_fields = ['cliente__email', 'cliente__nombre',
                     'cliente__apellido', 'cliente__no_documento']
    date_hierarchy = 'fecha_creacion'
    readonly_fields = ('fecha_creacion', 'fecha_ultima_modificacion')

    def nombre(self, obj):
        return obj.nombre

    def apellido(self, obj):
        return obj.apellido

    def get_queryset(self, request):
        querysetAux = super().get_queryset(request)
        return querysetAux.annotate(
            nombre=F('cliente__nombre'),
            apellido=F('cliente__apellido')
        )


@admin.register(cliente)
class datsClientsAdmin(admin.ModelAdmin):

    list_display = ('usuario', 'nombre_cliente', 'apellido_cliente')
    list_filter = ('usuario__estado',)
    list_display_links = ('usuario', 'nombre_cliente', 'apellido_cliente')
    autocomplete_fields = ['usuario']
    search_fields = ['usuario__email', 'usuario__nombre', 'usuario__apellido']

    def nombre_cliente(self, obj):
        return obj.nombre_cliente

    def apellido_cliente(self, obj):
        return obj.apellido_cliente

    def get_queryset(self, request):
        querysetAux = super().get_queryset(request)
        return querysetAux.annotate(nombre_cliente=F('usuario__nombre'), apellido_cliente=F('usuario__apellido'))


@admin.register(facturas)
class facturaAdmin(admin.ModelAdmin):

    list_filter = ('pago', 'fecha_creacion', 'metodo_pago')
    list_display = ('id_bill', 'nombre', 'plan', 'total_pagar', 'descargar')
    list_display_links = ('id_bill', 'plan', 'nombre')
    show_full_result_count = 50
    autocomplete_fields = ['plan']
    #raw_id_fields = ('plan' , )
    search_fields = ['nombre',  'id_bill']
    date_hierarchy = 'fecha_creacion'

    fieldsets = (
        ('Informacion de la factura', {'fields': ('pago', 'plan', 'total_recibido', 'total_pagar','total_devuelto', 'fecha_creacion', 'fecha_pago',
                                                  'fecha_limite_pago', 'metodo_pago', 'codigo_convenio', 'codigo_epy', 'pin_epy', 'numero_recibo')}),
        ('Informacion del plan', {'fields': (
            'id_plan', 'servicio', 'costo_del_plan', 'saldo_en_contra', 'saldo_a_favor')}),
        ('Informacion del cliente', {
         'fields': ('nombre',  'no_documento')}),
    )

    readonly_fields = ['total_pagar', 'fecha_creacion', 'fecha_limite_pago',  'metodo_pago', 'codigo_convenio', 'codigo_epy', 'pin_epy', 'numero_recibo', 'servicio',
                       'saldo_en_contra', 'saldo_a_favor', 'nombre', 'no_documento', 'costo_del_plan', 'total_devuelto', 'id_plan']

    class Media:
        css = {
            "all": ("navecomClient/css_project/style_admin.css", "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css")
        }
        js = ( 'navecomClient/js_project/ctrlFaturaAdmin.js',)

    def descargar(self, obj):
        return format_html('<i class="fa fa-file-pdf-o linkPdf downloadFact" id="downloadFact" ><a href="%s"> Descargar</a></i>'%reverse('downloadFact', args=[obj.id_bill]) )

    def nombre(self, obj):
        return "%s %s" % (obj.nombre, obj.apellido)

    def no_documento(self, obj):
        return obj.no_documento

    def servicio(self, obj):
        return categorias_servicio.objects.get(pk=obj.servicio)

    def costo_del_plan(self, obj):
        return obj.costo_del_plan

    def saldo_en_contra(self, obj):
        return obj.saldo_en_contra

    def saldo_a_favor(self, obj):
        return obj.saldo_a_favor

    def id_plan(self, obj):
        return obj.no_plan

    def get_queryset(self, request):
        querysetAux = super().get_queryset(request)
        return querysetAux.annotate(
            # informacion del plan
            no_plan=F('plan__id_plan'), servicio=F('plan__servicio'), costo_del_plan=F('plan__servicio__costo'), saldo_en_contra=F('plan__saldo_contra'), saldo_a_favor=F('plan__saldo_favor'),
            # informacion del cliente
            nombre=F('plan__contrato__cliente__nombre'), apellido=F('plan__contrato__cliente__apellido'), no_documento=F('plan__contrato__cliente__no_documento')
        )


@admin.register(plan)
class planAdmin(admin.ModelAdmin):

    list_filter = ('estado_plan', 'dia_inicio_pago', 'servicio')
    list_display = ('id_plan', 'nombre_cliente',
                    'servicio', 'precio_plan', 'estado_del_plan')
    list_display_links = ('id_plan', 'nombre_cliente',
                          'servicio', 'precio_plan')
    #raw_id_fields = ('', )
    search_fields = ['id_plan', 'nombre_cliente']

    readonly_fields = ['fecha_registro_plan', 'fecha_ultima_modificacion',
                       'dias_limites_de_pago', 'saldo_contra', 'saldo_favor', 'estado_plan']

    autocomplete_fields = ['contrato', 'servicio']
    filter_horizontal = ('montos_adicionales',
                         'descuentos_adicionales', 'novedades')

    def estado_del_plan(self, obj):
        color = {1: '74FF00', 2: 'FFF700', 3: 'FF0000', 4: '00FFA2'}
        return format_html('<span style="color: #898989; background-color:#{}; padding: 3px 10px; border-radius: 7px; font-weight: bold;">{}</span>',
                           color[obj.estado_plan.id_state_plan],
                           obj.estado_plan)

    def nombre_cliente(self, obj):
        return "%s %s" % (obj.nombre_cliente, obj.apellido_cliente)

    def precio_plan(self, obj):
        return obj.precio

    def get_queryset(self, request):
        querysetAux = super().get_queryset(request)
        return querysetAux.annotate(nombre_cliente=F('contrato__cliente__nombre'), apellido_cliente=F('contrato__cliente__apellido'), precio=F('servicio__costo'))


@admin.register(solicitudes_servicio)
class solitudServAdmin(admin.ModelAdmin):

    list_display = ('nombre', 'no_celular', 'fecha_solicitud')
    readonly_fields = ['email', 'nombre', 'no_celular',
                       'tel_fijo', 'direccion', 'fecha_solicitud', 'plan']
    list_filter = ('atendido',)


@admin.register(servicio)
class serviciosAdmin(admin.ModelAdmin):

    list_display = ('id_ser', 'nombre_servicio')
    list_display_links = ('id_ser', 'nombre_servicio')
    search_fields = ('nombre_servicio', 'oferta_servicio')


@admin.register(estados_usuario)
class estadosUsuarioAdmin(admin.ModelAdmin):
    list_display = ('id_state_usr', 'nombre_estado', 'descripcion')


@admin.register(estados_plan)
class estadoPlanAdmin(admin.ModelAdmin):
    list_display = ('id_state_plan', 'estado_plan', 'descripcion')


admin.site.register(monto_adicional)
admin.site.register(descuentos)
admin.site.register(empleado)
admin.site.register(novedades_plan)
admin.site.register(metodos_pago)
admin.site.register(tipo_usuario)
admin.site.register(Permission)
admin.site.register(zonas_servicio)
admin.site.register(contact_request)
