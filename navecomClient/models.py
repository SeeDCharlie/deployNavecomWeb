from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class AditionalAmount(models.Model):
    id_amount = models.AutoField(primary_key=True)
    name_amount = models.CharField(max_length=30, blank=True, null=True)
    description = models.CharField(max_length=60, blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    percentage = models.DecimalField(max_digits=4, decimal_places=3, blank=True, null=True)

    class Meta:
        db_table = 'aditional_amount'


class AmountList(models.Model):
    id_amount_aply = models.AutoField(primary_key=True)
    plan = models.ForeignKey('Plans', models.DO_NOTHING, db_column='plan')
    amount = models.ForeignKey(AditionalAmount, models.DO_NOTHING, db_column='amount')

    class Meta:
        db_table = 'amount_list'


class Bills(models.Model):
    id_bill = models.AutoField(primary_key=True)
    id_plan = models.ForeignKey('Plans', models.DO_NOTHING, db_column='id_plan')
    arrears_state = models.BooleanField()
    positive_balance = models.DecimalField(max_digits=9, decimal_places=2)
    negative_balance = models.DecimalField(max_digits=9, decimal_places=2)
    total_pay = models.DecimalField(max_digits=7, decimal_places=2)
    recovery_date = models.DateField()
    payment_date = models.DateField()
    payday_limit = models.DateField()
    payment_method = models.CharField(max_length=50)

    class Meta:
        db_table = 'bills'


class CategoryServices(models.Model):
    id_cat_ser = models.AutoField(primary_key=True)
    id_ser = models.ForeignKey('Services', models.DO_NOTHING, db_column='id_ser')
    service_complement = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'category_services'


class Contracts(models.Model):
    id_contract = models.AutoField(primary_key=True)
    contract_usr = models.ForeignKey('Users', models.DO_NOTHING, db_column='contract_usr')
    contract_status = models.BooleanField()
    registration_date = models.DateTimeField(blank=True, null=True)
    start_contract = models.DateField(blank=True, null=True)
    end_contract = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'contratcs'


class CustomStates(models.Model):
    id_state_custom = models.AutoField(primary_key=True)
    name_state = models.CharField(max_length=20, blank=True, null=True)
    description = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'customer_states'


class Customers(models.Model):
    id_customer = models.OneToOneField('Users', models.DO_NOTHING, db_column='id_customer')
    payment_method = models.ForeignKey('PaymentMethods', models.DO_NOTHING, db_column='payment_method')
    payment_account = models.CharField(max_length=50, blank=True, null=True)
    state = models.ForeignKey(CustomStates, models.DO_NOTHING, db_column='state')
    register_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'customers'


class DiscountList(models.Model):
    id_discount_aply = models.AutoField(primary_key=True)
    plan = models.ForeignKey('Plans', models.DO_NOTHING, db_column='plan')
    discount = models.ForeignKey('Discounts', models.DO_NOTHING, db_column='discount')

    class Meta:
        db_table = 'discount_list'


class Discounts(models.Model):
    id_discount = models.AutoField(primary_key=True)
    name_discount = models.CharField(max_length=30, blank=True, null=True)
    description = models.CharField(max_length=60, blank=True, null=True)
    conditions = models.CharField(max_length=80, blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    percentage = models.DecimalField(max_digits=4, decimal_places=3, blank=True, null=True)

    class Meta:
        db_table = 'discounts'


class Employees(models.Model):
    id_employe = models.OneToOneField('Users', models.DO_NOTHING, db_column='id_employe')
    entry_date = models.DateTimeField(blank=True, null=True)
    dismissal_date = models.DateTimeField(blank=True, null=True)
    description_work = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'employees'


class Novelties(models.Model):
    id_novel = models.AutoField(primary_key=True)
    plan = models.ForeignKey('Plans', models.DO_NOTHING, db_column='plan')
    name_novel = models.CharField(max_length=30, blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    opcional = models.CharField(max_length=50, blank=True, null=True)
    reg_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'novelties'


class PaymentMethods(models.Model):
    id_method = models.AutoField(primary_key=True)
    name_method = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'payment_methods'


class PlanStates(models.Model):
    id_state_plan = models.AutoField(primary_key=True)
    name_st = models.CharField(max_length=20, blank=True, null=True)
    description = models.CharField(max_length=60, blank=True, null=True)

    class Meta:
        db_table = 'plan_states'


class Plans(models.Model):
    id_plan = models.AutoField(primary_key=True)
    contract = models.ForeignKey(Contracts, models.DO_NOTHING, db_column='contract')
    contract_usr = models.ForeignKey('Users', models.DO_NOTHING, db_column='contract_usr')
    id_cat_ser = models.ForeignKey(CategoryServices, models.DO_NOTHING, db_column='id_cat_ser')
    state_plan = models.ForeignKey(PlanStates, models.DO_NOTHING, db_column='state_plan')
    instalation_plan = models.DateTimeField(blank=True, null=True)
    start_payment_date = models.DateField(blank=True, null=True)
    end_payment_date = models.DateField(blank=True, null=True)
    cancel_plan_date = models.DateTimeField(blank=True, null=True)
    ip_router = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'plans'


class RequestsServices(models.Model):
    id_request = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=60, blank=True, null=True)
    cell_phone = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    phone = models.DecimalField(max_digits=7, decimal_places=0, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=40, blank=True, null=True)
    regis_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'requests_services'


class Services(models.Model):
    id_ser = models.AutoField(primary_key=True)
    name_ser = models.CharField(max_length=50)
    service_offer = models.CharField(max_length=50)

    class Meta:
        db_table = 'services'


class TypeUsers(models.Model):
    id_ty_us = models.AutoField(primary_key=True)
    name_t_u = models.CharField(max_length=50)

    class Meta:
        db_table = 'type_users'

class usersManager(BaseUserManager):
    def create_superuser(self, email, nickname, f_name, l_name, id_ty_us, password):
        usuario = self.create_user(email = email, nickname = nickname, f_name = f_name, l_name = l_name, id_ty_us = id_ty_us, password = password)
        usuario.usuario_administrador = True
        usuario.save()
        return usuario

    def create_user(self, email, nickname, f_name, l_name, id_ty_us, password ):
        if not email:
            raise ValueError('el usuario debe tener un correo electronico')
        else :
            usuario = self.model(email = self.normalize_email(email), nickname = nickname , f_name = f_name, l_name = l_name, id_ty_us = TypeUsers.objects.get(pk=id_ty_us))
            usuario.set_password(password)
            usuario.save()
            return usuario

class users(AbstractBaseUser):
    id_user = models.AutoField(primary_key=True)
    id_ty_us = models.ForeignKey(TypeUsers, models.DO_NOTHING, db_column='id_ty_us')
    document_usr = models.DecimalField(max_digits=13, decimal_places=0, null=True)
    f_name = models.CharField(max_length=50)
    l_name = models.CharField(max_length=50)
    email = models.CharField(unique=True, max_length=100)
    cell_number = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    phone = models.DecimalField(max_digits=7, decimal_places=0, blank=True, null=True)
    address = models.CharField(max_length=50, null=True)
    neighborhood = models.CharField(max_length=50, blank=True, null=True)
    home_reference = models.CharField(max_length=50, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    nickname = models.CharField(max_length=30, blank=True, null=True)
    #passw = models.CharField(db_column='passw', max_length=100, blank=True, null=True)  # Field renamed because it was a Python reserved word.
    token_key = models.CharField(max_length=300, blank=True, null=True)
    register_date = models.DateTimeField(blank=True, auto_now=True, null = True)
    state_usr = models.ForeignKey('UsrStates', models.DO_NOTHING, db_column='state_usr', null = True)

    usuario_administrador = models.BooleanField(default=False)
    objects = usersManager()


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [ 'nickname', 'f_name', 'l_name', 'id_ty_us' ]

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj = None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.usuario_administrador

    class Meta:
        db_table = 'users'



class UsrStates(models.Model):
    id_state_usr = models.AutoField(primary_key=True)
    name_state = models.CharField(max_length=20, blank=True, null=True)
    description = models.CharField(max_length=50, blank=True, null=True)
    
    class Meta:
        db_table = 'usr_states'
