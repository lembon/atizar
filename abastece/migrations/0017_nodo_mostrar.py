# Generated by Django 3.1.2 on 2021-10-28 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abastece', '0016_auto_20211024_1211'),
    ]

    operations = [
        migrations.AddField(
            model_name='nodo',
            name='mostrar',
            field=models.BooleanField(default=True, verbose_name='Mostrar en listado'),
        ),
    ]