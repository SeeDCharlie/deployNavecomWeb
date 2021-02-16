# Generated by Django 3.1.4 on 2021-02-02 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('navecomClient', '0008_auto_20210131_1435'),
    ]

    operations = [
        migrations.RenameField(
            model_name='facturas',
            old_name='estado_factura',
            new_name='pago',
        ),
        migrations.RemoveField(
            model_name='plan',
            name='fecha_inicio_pago',
        ),
        migrations.RemoveField(
            model_name='plan',
            name='fecha_limite_pago',
        ),
        migrations.AddField(
            model_name='plan',
            name='days_limit',
            field=models.IntegerField(blank=True, db_column='days_limit', default=5, null=True),
        ),
        migrations.AddField(
            model_name='plan',
            name='dia_inicio_pago',
            field=models.IntegerField(blank=True, db_column='start_payment_day', default=30, null=True),
        ),
    ]
