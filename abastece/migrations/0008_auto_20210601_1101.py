# Generated by Django 3.1.2 on 2021-06-01 14:01

import datetime

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('abastece', '0007_auto_20210531_2331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime.now, editable=False, verbose_name='fecha y hora'),
        ),
    ]
