# Generated by Django 3.1.4 on 2021-03-30 00:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('navecomClient', '0017_auto_20210330_0511'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plan',
            name='descuentos_adicionales',
        ),
    ]
