# Generated by Django 3.1.4 on 2021-04-09 22:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('navecomClient', '0026_auto_20210410_0332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='montos_plan',
            name='monto_adicional',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.DO_NOTHING, to='navecomClient.monto_adicional'),
        ),
    ]
