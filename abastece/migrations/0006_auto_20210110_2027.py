# Generated by Django 3.1.2 on 2021-01-10 23:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('abastece', '0005_auto_20210110_1525'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductoVariedadCiclo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('disponible', models.IntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name='itempedido',
            name='producto_variedad',
        ),
        migrations.RemoveField(
            model_name='pedido',
            name='ciclo',
        ),
        migrations.AddField(
            model_name='ciclo',
            name='aporte_central',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='ciclo',
            name='aporte_deposito',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='ciclo',
            name='aporte_logistica',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='ciclo',
            name='aporte_nodo',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='ciclo',
            name='productos',
            field=models.ManyToManyField(related_name='ciclos', through='abastece.ProductoCiclo', to='abastece.Producto'),
        ),
        migrations.AddField(
            model_name='productociclo',
            name='costo_financiero',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productociclo',
            name='costo_postproceso',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productociclo',
            name='costo_produccion',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productociclo',
            name='costo_transporte',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='producto',
            name='unidad',
            field=models.CharField(choices=[('U', 'unidades'), ('g', 'gramos'), ('kg', 'kilogramos'), ('cm3', 'centímetros cúbicos'), ('ml', 'mililitros'), ('l', 'litros'), ('m', 'metros')], max_length=100),
        ),
        migrations.AddConstraint(
            model_name='productociclo',
            constraint=models.UniqueConstraint(fields=('ciclo', 'producto'), name='unico producto por ciclo'),
        ),
        migrations.AddField(
            model_name='productovariedadciclo',
            name='ciclo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='abastece.ciclo'),
        ),
        migrations.AddField(
            model_name='productovariedadciclo',
            name='producto_variedad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='abastece.productovariedad'),
        ),
        migrations.AddField(
            model_name='itempedido',
            name='producto_variedad_ciclo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='abastece.productovariedadciclo'),
            preserve_default=False,
        ),
    ]
