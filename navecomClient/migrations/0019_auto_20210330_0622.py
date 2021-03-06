# Generated by Django 3.1.4 on 2021-03-30 01:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('navecomClient', '0018_remove_plan_descuentos_adicionales'),
    ]

    operations = [
        migrations.AlterField(
            model_name='montos_plan',
            name='monto_adicional',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='navecomClient.monto_adicional'),
        ),
        migrations.AlterField(
            model_name='montos_plan',
            name='plan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='navecomClient.plan'),
        ),
        migrations.CreateModel(
            name='descuentos_plan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no_aplicado', models.IntegerField(default=0)),
                ('descuentos', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='navecomClient.descuentos')),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='navecomClient.plan')),
            ],
            options={
                'verbose_name': 'descuento del plan',
                'verbose_name_plural': 'descuentos de los planes',
                'db_table': 'descuentos_plan',
            },
        ),
        migrations.AddField(
            model_name='plan',
            name='descuentos',
            field=models.ManyToManyField(blank=True, through='navecomClient.descuentos_plan', to='navecomClient.descuentos'),
        ),
    ]
