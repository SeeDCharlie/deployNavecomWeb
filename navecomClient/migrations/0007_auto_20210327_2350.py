# Generated by Django 3.1.4 on 2021-03-27 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('navecomClient', '0006_auto_20210327_1122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facturas',
            name='fecha_pago',
            field=models.DateTimeField(blank=True, db_column='payment_date', null=True),
        ),
    ]