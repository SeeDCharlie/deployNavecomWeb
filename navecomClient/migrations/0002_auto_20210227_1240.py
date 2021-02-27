# Generated by Django 3.1.4 on 2021-02-27 07:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('navecomClient', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facturas',
            name='fecha_limite_pago',
            field=models.DateTimeField(blank=True, db_column='payday_limit', default=django.utils.timezone.now, null=True),
        ),
    ]
