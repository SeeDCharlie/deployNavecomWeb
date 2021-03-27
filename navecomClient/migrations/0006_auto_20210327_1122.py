# Generated by Django 3.1.4 on 2021-03-27 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('navecomClient', '0005_auto_20210326_0353'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='facturas',
            name='codigo_convenio',
        ),
        migrations.RemoveField(
            model_name='facturas',
            name='codigo_epy',
        ),
        migrations.RemoveField(
            model_name='facturas',
            name='numero_recibo',
        ),
        migrations.RemoveField(
            model_name='facturas',
            name='pin_epy',
        ),
        migrations.AddField(
            model_name='facturas',
            name='codigo_aprobacion_payco',
            field=models.CharField(blank=True, db_column='cod_apro_payco', max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='facturas',
            name='numero_recibo_transaccion',
            field=models.CharField(blank=True, db_column='id_invoice_payco', max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='facturas',
            name='referencia_payco',
            field=models.CharField(blank=True, db_column='ref_payco', max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='facturas',
            name='type_method',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
