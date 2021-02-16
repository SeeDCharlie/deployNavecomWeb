# Generated by Django 3.1.4 on 2021-02-04 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('navecomClient', '0018_auto_20210204_1037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='saldo_contra',
            field=models.DecimalField(db_column='negative_balance', decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='plan',
            name='saldo_favor',
            field=models.DecimalField(db_column='positive_balance', decimal_places=2, default=0, max_digits=10, null=True),
        ),
    ]
