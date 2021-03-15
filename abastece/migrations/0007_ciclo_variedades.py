# Generated by Django 3.1.2 on 2021-03-14 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abastece', '0006_auto_20210110_2027'),
    ]

    operations = [
        migrations.AddField(
            model_name='ciclo',
            name='variedades',
            field=models.ManyToManyField(related_name='ciclos', through='abastece.ProductoVariedadCiclo', to='abastece.ProductoVariedad'),
        ),
    ]
