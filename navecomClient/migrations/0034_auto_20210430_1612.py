# Generated by Django 3.1.4 on 2021-04-30 21:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('navecomClient', '0033_auto_20210430_1342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='estado_plan',
            field=models.ForeignKey(db_column='state_plan', default=4, on_delete=django.db.models.deletion.DO_NOTHING, to='navecomClient.estados_plan'),
        ),
    ]
