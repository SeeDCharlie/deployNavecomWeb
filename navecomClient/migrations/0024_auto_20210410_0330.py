# Generated by Django 3.1.4 on 2021-04-09 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('navecomClient', '0023_auto_20210402_2032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='ip_dir',
            field=models.CharField(blank=True, default=None, max_length=17),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='plan',
            name='mac',
            field=models.CharField(blank=True, max_length=25),
        ),
        migrations.AlterField(
            model_name='plan',
            name='marca',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='plan',
            name='mascara',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='plan',
            name='nuevo',
            field=models.IntegerField(blank=True, choices=[(1, 'SI'), (2, 'NO')], default=1, null=True),
        ),
        migrations.AlterField(
            model_name='plan',
            name='referencia',
            field=models.CharField(blank=True, max_length=60),
        ),
        migrations.AlterField(
            model_name='plan',
            name='serial',
            field=models.CharField(blank=True, max_length=35),
        ),
    ]