# Generated by Django 3.1.2 on 2020-11-20 18:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('abastece', '0003_auto_20201120_0015'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nodo',
            name='miembros',
        ),
        migrations.AddField(
            model_name='contacto',
            name='nombre_fantasia',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='nodo',
            name='domicilio_recepcion',
            field=models.ForeignKey(blank=True, help_text='Solo cuando la mercadería se recibe en un domicilio diferente del de funcionamiento.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='domicilio_recepcion', to='abastece.domicilio'),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='consumidor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='abastece.membresia'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='envase',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='producto',
            name='titulo',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.CreateModel(
            name='ImagenContacto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contacto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='abastece.contacto')),
            ],
        ),
    ]
