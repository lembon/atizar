# Generated by Django 3.1.2 on 2021-08-28 13:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('abastece', '0009_contacto_usuario'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='nombre',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
    ]