from django.db import models
from django.contrib.auth.models import  BaseUserManager,AbstractBaseUser, Permission, Group, PermissionsMixin
from django.utils import timezone

class contact_request(models.Model):
    nombre = models.CharField(max_length = 40, db_column = 'name')
    email = models.EmailField(max_length=300)
    cel = models.IntegerField(default=0, db_column='celphone', null = True )
    asunto = models.CharField(max_length=50, null = True)
    mensaje = models.CharField(max_length=600, db_column='message')
    atendida = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre
    
    class Meta:
        db_table = 'contact_request'
        verbose_name = "Solicitud de Contacto"
        verbose_name_plural = "Solicitudes de contacto"

class zonas_servicio(models.Model):
    id_zone = models.AutoField(primary_key = True)
    nombre = models.CharField(max_length = 40, db_column = 'name' )

    def __str__(self):
        return self.nombre
    
    class Meta:
        db_table = 'service_zones'
        verbose_name = "Zona de Servicio"
        verbose_name_plural = "Zonas de Servicios"

class monto_adicional(models.Model):
    id_amount = models.AutoField(primary_key=True)
    nombre_monto = models.CharField(max_length=30, blank=True, null=True, db_column='name_amount')
    descripcion = models.CharField(max_length=60, blank=True, null=True, db_column='description')
    precio = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True, db_column='price')
    porcentaje = models.DecimalField(max_digits=4, decimal_places=3, blank=True, null=True, db_column='percentage')
    


    def __str__(self):
        return "%s | $ %d"%(self.nombre_monto,self.precio) 

    class Meta:
        db_table = 'aditional_amount'
        verbose_name = "monto adicional"
        verbose_name_plural = "montos adicionales"

class facturas(models.Model):
    id_bill = models.AutoField(primary_key=True)
    plan = models.ForeignKey('plan', models.DO_NOTHING, db_column='id_plan')
    pago = models.BooleanField(db_column = 'arrears_state', default=0)
    total_recibido = models.DecimalField(max_digits= 9, decimal_places=2, blank=True, null=True, db_column='balance_received')
    total_pagar = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True, db_column='total_pay')
    total_devuelto = models.DecimalField(max_digits=9, decimal_places=2, blank=True,null=True, db_column='balance_returned')
    metodo_pago = models.ForeignKey('metodos_pago', models.DO_NOTHING, default=5, db_column='payment_method')
    primera_factura = models.BooleanField(db_column = 'first_fact', default=0)

    type_method = models.CharField(max_length=20, blank=True, null=True)  
    referencia_payco = models.CharField(max_length=250, blank=True, null=True, db_column='ref_payco')
    codigo_aprobacion_payco = models.CharField(max_length=250, blank=True, null=True, db_column='cod_apro_payco')
    numero_recibo_transaccion = models.CharField(max_length=250, blank=True, null=True, db_column='id_invoice_payco')
    pin_payco = models.CharField(max_length=30, blank=True, null=True)
    
    fecha_creacion = models.DateField(blank=True, null=True, auto_now_add=True, db_column='recovery_date')
    fecha_pago = models.DateTimeField(blank=True, null=True, db_column='payment_date')
    fecha_limite_pago = models.DateField(blank=True, null = True, db_column='payday_limit')

    observacion = models.CharField(max_length=400, null=True, blank=True)

    def __str__(self):
        return "%d | %s"%(self.id_bill, str(self.plan))

    class Meta:
        db_table = 'bills'
        verbose_name = "factura"
        verbose_name_plural = "facturas"

class categorias_servicio(models.Model):
    id_cat_ser = models.AutoField(primary_key=True)
    zonas = models.ManyToManyField(zonas_servicio, db_column = 'zones' )
    servicio = models.ForeignKey('servicio', models.DO_NOTHING, db_column='servicio')
    complemento_servicio = models.CharField(max_length=50, db_column='service_complement')
    descripcion = models.TextField(max_length=250,db_column='description')
    costo = models.DecimalField(max_digits=10, decimal_places=2, db_column='price')

    def __str__(self):
        return "%s | %s | %s"%(self.servicio, self.complemento_servicio, self.getZonas())

    def getZonas(self):
        return ', '.join(name_z.__str__() for name_z in self.zonas.all())

    class Meta:
        db_table = 'category_services'
        verbose_name = "plan de servicio"
        verbose_name_plural = "planes de servicios"


class contrato(models.Model):
    id_contract = models.AutoField(primary_key=True)
    cliente = models.ForeignKey('usuario', models.DO_NOTHING, db_column='contract_usr')
    Fotocopia_cedula = models.BooleanField(default=False, db_column='foto_cedula')
    activo = models.BooleanField(db_column='contract_status',default=True)
    fecha_creacion = models.DateField( blank=True, null = True, auto_now_add=True, db_column='registration_date')
    fecha_inicio_contrato = models.DateField(blank=False, null=False, db_column='start_contract')
    fecha_minima_permanencia = models.DateField(blank=True, null = True, db_column='end_contract')
    fecha_ultima_modificacion = models.DateTimeField(blank=True, null = True, auto_now=True, db_column='last_modify')

    def __str__(self):
        return "%d | %s | CC. %d"%(self.id_contract, (self.cliente.nombre + ' ' +self.cliente.apellido), self.cliente.no_documento )

    class Meta:
        db_table = 'contratcs'
        verbose_name = "contrato"
        verbose_name_plural = "contratos"


class cliente(models.Model):
    usuario = models.OneToOneField('usuario', models.DO_NOTHING, db_column='id_customer')
    metodo_pago = models.ForeignKey('metodos_pago', models.DO_NOTHING, db_column='payment_method')
    no_cuenta_pago = models.CharField(max_length=50, blank=True, null=True, db_column='payment_account')
    fecha_modificacion = models.DateTimeField(blank=True, auto_now=True, null=True, db_column='register_date')

    def __str__(self):
        return str(self.usuario)

    class Meta:
        db_table = 'customers'
        verbose_name = "datos del cliente"
        verbose_name_plural = "datos de los clientes"


class descuentos(models.Model):
    id_discount = models.AutoField(primary_key=True)
    nombre_descuento = models.CharField(max_length=30, blank=True, null=True, db_column='name_discount')
    descripcion = models.CharField(max_length=150, blank=True, null=True, db_column='description')
    condiciones_restricciones = models.CharField(max_length=80, blank=True, null=True, db_column='conditions')
    precio = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True,db_column='price')
    porcentaje = models.DecimalField(max_digits=4, decimal_places=3, blank=True, null=True, db_column='percentage')

    def __str__(self):
        return self.nombre_descuento

    class Meta:
        db_table = 'discounts'
        verbose_name = "descuento"
        verbose_name_plural = "descuentos"


class empleado(models.Model):
    empleado = models.OneToOneField('usuario', models.DO_NOTHING, db_column='id_employe')
    fecha_ingreso = models.DateTimeField(blank=True, null=True, db_column='entry_date')
    fecha_despido = models.DateTimeField(blank=True, null=True, db_column='dismissal_date')
    descripcion_cargo = models.CharField(max_length=100, blank=True, null=True, db_column='description_work')

    def __str__(self):
        return "%s"%str(self.id_employe)

    class Meta:
        db_table = 'employees'
        verbose_name = "datos del empleado"
        verbose_name_plural = "datos de empleados"


class novedades_plan(models.Model):
    id_novel = models.AutoField(primary_key=True)
    nombre_novedad = models.CharField(max_length=30, db_column='name_novel')
    descripcion = models.CharField(max_length=100, db_column='description')
    opcional = models.CharField(max_length=50, blank=True, null=True)
    fecha_actualizacion = models.DateTimeField(blank=True,auto_now=True, null=True, db_column='reg_date')

    def __str__(self):
        return "%s | %s"%(self.nombre_novedad, self.descripcion)

    class Meta:
        db_table = 'novelties'
        verbose_name = "novedad"
        verbose_name_plural = "novedades de los planes"


class metodos_pago(models.Model):
    id_method = models.AutoField(primary_key=True)
    nombre_metodo = models.CharField(max_length=50, blank=True, null=True, db_column='name_method')

    def __str__(self):
        return self.nombre_metodo

    class Meta:
        db_table = 'payment_methods'
        verbose_name = "metodo de pago"
        verbose_name_plural = "metodos de pago"


class estados_plan(models.Model):
    id_state_plan = models.AutoField(primary_key=True)
    estado_plan = models.CharField(max_length=20, blank=True, null=True, db_column='name_st')
    descripcion = models.CharField(max_length=60, blank=True, null=True, db_column='description')

    def __str__(self):
        return self.estado_plan

    class Meta:
        db_table = 'plan_states'
        verbose_name = "estado del plan"
        verbose_name_plural = "estados de planes"

class descuentos_plan(models.Model):
    plan = models.ForeignKey('plan', models.DO_NOTHING)
    descuentos = models.ForeignKey('descuentos', models.DO_NOTHING)
    factura = models.ForeignKey('facturas', models.DO_NOTHING, null=True)
    no_meses_aplica = models.PositiveIntegerField(default=1)
    ESTADOS = (('p', 'Pendiente'), ('c','Culminado') )
    estado = models.CharField(default=1,db_column='descuentos_estado',max_length=15, choices= ESTADOS)
    fecha_creacion = models.DateField(auto_now_add=True, blank=True, null=True)
    fecha_modificacion = models.DateField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return str(self.descuentos) + " " + str(self.plan)

    class Meta:
        db_table = 'descuentos_plan'
        verbose_name = "descuento del plan"
        verbose_name_plural = "descuentos adicionales para planes"

class montos_plan(models.Model):
    monto_adicional = models.ForeignKey('monto_adicional',models.DO_NOTHING, default=3)
    plan = models.ForeignKey('plan', models.DO_NOTHING)
    factura = models.ForeignKey('facturas', models.DO_NOTHING, null=True)
    no_meses_aplica = models.PositiveIntegerField(default=1)
    ESTADOS = (('p', 'Pendiente'), ('c','Culminado') )
    estado = models.CharField(default=1,db_column='estado_monto',max_length=15, choices= ESTADOS)
    fecha_creacion = models.DateField(auto_now_add=True, blank=True, null=True)
    fecha_modificacion = models.DateField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return str(self.monto_adicional) + " " + str(self.plan)

    class Meta:
        db_table = 'montos_plan'
        verbose_name = "monto del plan"
        verbose_name_plural = "montos adicionales para planes"

class plan(models.Model):
    id_plan = models.AutoField(primary_key=True)
    contrato = models.ForeignKey(contrato, models.DO_NOTHING, db_column='contract')
    servicio = models.ForeignKey(categorias_servicio, models.DO_NOTHING, db_column='id_cat_ser')
    estado_plan = models.ForeignKey(estados_plan, models.DO_NOTHING,default=4, db_column='state_plan')
    DIAS_DE_PAGO = (('1',"1-5"), ('15',"15-20"))
    dia_inicio_pago = models.CharField( max_length=6, db_column='start_payment_day', choices=DIAS_DE_PAGO )
    dias_limites_de_pago = models.IntegerField(default=5, blank=True, null=True, db_column='days_limit' )
    direccion_recidencial = models.CharField(max_length=300, blank=False, null=False)

    #caracteristicas adicionales
    novedades = models.ManyToManyField(novedades_plan, blank=True)
    saldo_contra = models.DecimalField(max_digits=10, decimal_places=2, default= 0, db_column='negative_balance')
    saldo_favor = models.DecimalField(max_digits=10, decimal_places=2, default = 0, db_column='positive_balance')

    #DATOS DEL ROUTER
    marca = models.CharField(max_length=300, blank=True, null=True, default="tenda")
    ip_dir = models.CharField(max_length=17, blank=True, null=True)
    mascara = models.CharField(max_length=10, blank=True, null=True)
    serial = models.CharField(max_length=35, blank=True, null=True)
    mac = models.CharField(max_length=25, blank=True, null=True)
    referencia = models.CharField(max_length=60, blank=True, null=True)
    nuevo = models.IntegerField(blank=True, null=True, choices=((1,'SI'),(2,'NO')), default=1)

    fecha_instalacion = models.DateTimeField( db_column='instalation_date')
    fecha_registro_plan = models.DateTimeField(blank=True, null=True, auto_now_add=True, db_column='date_start_plan')
    fecha_fin_plan = models.DateTimeField( db_column='date_end_plan', null=True, blank=True)
    fecha_cancelacion = models.DateTimeField(blank=True, null=True, db_column='cancel_plan_date')
    fecha_ultima_modificacion = models.DateTimeField(blank=True, null = True, auto_now=True, db_column='last_modify')

    def __str__(self):
        clientPlan = self.contrato.cliente
        return "%s | %s | %s %s | $ %d "%(self.id_plan, str(self.servicio), str(clientPlan.nombre) , str(clientPlan.apellido), self.servicio.costo )

    class Meta:
        db_table = 'plans'
        verbose_name = "plan"
        verbose_name_plural = "planes contratados"


class solicitudes_servicio(models.Model):
    id_request = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=60, blank=True, null=True, db_column='fname')
    no_celular = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True, db_column='cell_phone')
    tel_fijo = models.DecimalField(max_digits=7, decimal_places=0, blank=True, null=True, db_column='phone')
    email = models.CharField(max_length=50, blank=True, null=True, db_column='email')
    direccion = models.CharField(max_length=40, blank=True, null=True, db_column='address')
    fecha_solicitud = models.DateTimeField(blank=True,  auto_now_add=True, null = True, db_column='regis_date')
    plan = models.ForeignKey(categorias_servicio, models.DO_NOTHING, db_column='id_plan', null=True )
    atendido = models.BooleanField(default=False, db_column='check_soli')

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'requests_services'
        verbose_name = "solicitud de servicio"
        verbose_name_plural = "solicitudes de servicios"


class servicio(models.Model):
    id_ser = models.AutoField(primary_key=True)
    nombre_servicio = models.CharField(max_length=50, db_column='name_ser')
    oferta_servicio = models.CharField(max_length=50, db_column='service_offer')

    def __str__(self):
        return self.nombre_servicio

    class Meta:
        db_table = 'services'
        verbose_name = "servicio"
        verbose_name_plural = "servicios"


class tipo_usuario(models.Model):
    id_ty_us = models.AutoField(primary_key=True)
    tipo_usuario = models.CharField(max_length=50, db_column='name_t_u')

    def __str__(self):
        return self.tipo_usuario

    class Meta:
        db_table = 'type_users'
        verbose_name = "tipo de usuario"
        verbose_name_plural = "tipos de usuarios"

class usersManager(BaseUserManager):
    def create_superuser(self, email,tipo_usuario,no_documento, nombre, apellido, no_celular, tel_fijo,direccion, barrio, referencia_vivienda, nickname, estado, password):
        usuario = self.create_user(email = email, no_documento = no_documento , nombre = nombre, apellido = apellido, no_celular = no_celular, tel_fijo = tel_fijo,direccion = direccion, barrio = barrio, referencia_vivienda = referencia_vivienda, nickname = nickname,  tipo_usr = tipo_usuario, estado = estado, password = password)
        usuario.usuario_administrador = True
        usuario.save()
        return usuario

    def create_user(self, email, tipo_usr,no_documento, nombre, apellido, no_celular, tel_fijo,direccion, barrio, referencia_vivienda, nickname, password, estado ):
        if not email:
            raise ValueError('el usuario debe tener un correo electronico')
        else :
            usuario = self.model(email = self.normalize_email(email),no_documento = no_documento , nombre = nombre, apellido = apellido, no_celular = no_celular, tel_fijo = tel_fijo,direccion = direccion, barrio = barrio, referencia_vivienda = referencia_vivienda, nickname = nickname, estado = estados_usuario.objects.get(pk = estado),  tipo_usuario = tipo_usuario.objects.get(pk=tipo_usr))
            usuario.set_password(password)
            usuario.save()
            return usuario

class usuario(AbstractBaseUser, PermissionsMixin):
    id_user = models.AutoField(primary_key=True)
    tipo_usuario = models.ForeignKey(tipo_usuario, models.DO_NOTHING, default=3, db_column='id_ty_us')
    no_documento = models.DecimalField(max_digits=13, decimal_places=0, null=True, db_column='document_usr')
    nombre = models.CharField(max_length=50, db_column='f_name')
    apellido = models.CharField(max_length=50, db_column='l_name')
    email = models.CharField(unique=True, max_length=100)
    no_celular = models.DecimalField(max_digits=10, decimal_places=0, null=True, db_column='cell_number')
    tel_fijo = models.DecimalField(max_digits=7, decimal_places=0, blank=True, null=True, db_column='phone')
    direccion = models.CharField(max_length=50, null=True, db_column='address')
    barrio = models.CharField(max_length=50, blank=True, null=True, db_column='neighborhood')
    referencia_vivienda = models.CharField(max_length=50, blank=True, null=True, db_column='home_reference')
    fecha_cumpleaños = models.DateField(blank=True, null=True, db_column='dob')
    nickname = models.CharField(max_length=30, blank=True, null=True)
    token_key = models.CharField(max_length=300, blank=True, null=True)
    fecha_registro = models.DateTimeField(blank=True, auto_now=True, null = True, db_column='register_date')
    estado = models.ForeignKey('estados_usuario', models.DO_NOTHING, default=1,  db_column='state_usr', null = True)
    
    usuario_administrador = models.BooleanField(default=False)
    objects = usersManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [ 'tipo_usuario','no_documento', 'nombre', 'apellido', 'no_celular', 'tel_fijo','direccion', 'barrio', 'referencia_vivienda', 'estado', 'nickname' ]

    def __str__(self):
        return " %d | %s %s | CC. %d"%(self.id_user , self.nombre, self.apellido, self.no_documento)
    
    """def has_perm(self, perm, obj = None):
        return True

    def has_module_perms(self, app_label):
        return True
    """
    @property
    def is_staff(self):
        return self.usuario_administrador

    class Meta:
        db_table = 'users'
        app_label = 'navecomClient'
        verbose_name = "usuario"
        verbose_name_plural = "usuarios"



class estados_usuario(models.Model):
    id_state_usr = models.AutoField(primary_key=True)
    nombre_estado = models.CharField(max_length=20, blank=True, null=True, db_column='name_st')
    descripcion = models.CharField(max_length=50, blank=True, null=True, db_column='description')
    

    def __str__(self):
        return self.nombre_estado

    class Meta:
        db_table = 'usr_states'
        verbose_name = "estado del usuario"
        verbose_name_plural = "estados de los usuarios"



class logsnavecomsystem(models.Model):
    log_name = models.CharField(max_length=50)
    log_description = models.CharField(max_length=800)
    fecha_registro = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = 'logsnavecomsystem'
        verbose_name = "info del sistema"
        verbose_name_plural = "informacion del sistema"