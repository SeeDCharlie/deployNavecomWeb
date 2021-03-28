# Generated by Django 3.1.4 on 2021-03-28 21:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('navecomClient', '0009_auto_20210329_0239'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='router',
            field=models.ForeignKey(db_column='router', default=None, on_delete=django.db.models.deletion.DO_NOTHING, to='navecomClient.routers'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='routers',
            name='cantidad',
            field=models.SmallIntegerField(db_column='cant', default=1),
        ),
    ]