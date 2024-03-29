from django.db.models import Sum

from abastece.models import Nodo, Pedido, ItemPedido, ProductoCiclo, ProductoVariedad, ProductoVariedadCiclo, Contacto

TOTALES_RESUMEN = {'Costo Produccion': '=SUMA.PRODUCTO($E2:$E{filas};F2:F{filas})',
                   'Costo Transporte': '=SUMA.PRODUCTO($E2:$E{filas};G2:G{filas})',
                   'Costo Financiero': '=SUMA.PRODUCTO($E2:$E{filas};H2:H{filas})',
                   'Costo Postproceso': '=SUMA.PRODUCTO($E2:$E{filas};I2:I{filas})',
                   'A Nodos': '=SUMA.PRODUCTO($E2:$E{filas};J2:J{filas})',
                   'Logistica': '=SUMA.PRODUCTO($E2:$E{filas};K2:K{filas})',
                   'A la red': '=SUMA.PRODUCTO($E2:$E{filas};L2:L{filas})',
                   'A depositos': '=SUMA.PRODUCTO($E2:$E{filas};M2:M{filas})',
                   'Precio final': '=SUMA.PRODUCTO($E2:$E{filas};N2:N{filas})',
                   'Importe Total': '=SUMA(O2:O{filas})',
                   }


def remitos_nodos(ciclo):
    return [remito_nodo(ciclo, nodo) for nodo in Nodo.objects.all()]


def remito_nodo(ciclo, nodo):
    pedidos = Pedido.objects.filter(timestamp__range=(ciclo.inicio, ciclo.cierre), consumidor__nodo=nodo)
    items = ItemPedido.objects.filter(pedido__in=pedidos)
    items_agrupados = list(items.values('producto_variedad_ciclo__producto_variedad',
                                        'producto_variedad_ciclo__producto_variedad__descripcion',
                                        'producto_variedad_ciclo__producto_variedad__producto',
                                        )
                           .annotate(Sum('cantidad')))
    remito = {'importe_total': 0, 'importe_para_nodo': 0}
    for item in items_agrupados:
        item['producto_ciclo'] = ProductoCiclo.objects \
            .get(producto__pk=item['producto_variedad_ciclo__producto_variedad__producto'],
                 ciclo=ciclo)
        item['importe_nodo'] = item['producto_ciclo'].aporte_nodo * item['cantidad__sum']
        item['importe'] = item['producto_ciclo'].precio * item['cantidad__sum']
        remito['importe_total'] += item['importe']
        remito['importe_para_nodo'] += item['importe_nodo']
    remito['items'] = items_agrupados
    remito['importe_para_central'] = remito['importe_total'] - remito['importe_para_nodo']
    remito['nodo'] = nodo
    remito['ciclo'] = ciclo
    return remito


def remitos_productores(ciclo):
    return [remito_productor(ciclo, productor) for productor in Contacto.objects.all()]


def remito_productor(ciclo, productor):
    items = ItemPedido.objects.filter(pedido__timestamp__range=(ciclo.inicio, ciclo.cierre),
                                      producto_variedad_ciclo__producto_variedad__producto__productor=productor) \
        .order_by('producto_variedad_ciclo__producto_variedad')
    items_agrupados = list(items.values('producto_variedad_ciclo__producto_variedad', )
                           .annotate(Sum('cantidad')))
    remito = {'importe_total': 0}
    for item in items_agrupados:
        item['producto_variedad'] = ProductoVariedad.objects.get(pk=item['producto_variedad_ciclo__producto_variedad'])
        item['importe'] = item['producto_variedad'].producto.costo_produccion * item['cantidad__sum']
        remito['importe_total'] += item['importe']
    remito['items'] = items_agrupados
    remito['productor'] = productor
    remito[ciclo] = ciclo
    return remito


def resumen_post_proceso(ciclo):
    items = ItemPedido.objects.filter(pedido__timestamp__range=(ciclo.inicio, ciclo.cierre),
                                      producto_variedad_ciclo__producto_variedad__producto__costo_postproceso__gt=0) \
        .order_by('producto_variedad_ciclo__producto_variedad')
    items_agrupados = list(items.values('producto_variedad_ciclo__producto_variedad', )
                           .annotate(Sum('cantidad')))
    resumen = {'total': 0}
    for item in items_agrupados:
        item['producto_variedad'] = ProductoVariedad.objects.get(pk=item['producto_variedad_ciclo__producto_variedad'])
        item['importe'] = item['producto_variedad'].producto.costo_postproceso * item['cantidad__sum']
        resumen['total'] += item['importe']
    resumen['items'] = items_agrupados
    return resumen


def resumen_pedidos(ciclo):
    items_pedidos = ItemPedido.objects.filter(pedido__timestamp__range=(ciclo.inicio, ciclo.cierre)) \
        .order_by('producto_variedad_ciclo__producto_variedad__producto__productor')
    items_agrupados = list(items_pedidos.values(
        'producto_variedad_ciclo',
        'producto_variedad_ciclo__producto_variedad',
        'producto_variedad_ciclo__producto_variedad__descripcion',
        'producto_variedad_ciclo__producto_variedad__producto__titulo',
        'producto_variedad_ciclo__producto_variedad__producto__productor__nombre_fantasia',
    )
                           .annotate(Sum('cantidad')))
    for item in items_agrupados:
        producto_ciclo = ProductoVariedadCiclo.objects.get(pk=item['producto_variedad_ciclo']).producto_ciclo
        del item['producto_variedad_ciclo']
        item['Id Variedad'] = item.pop('producto_variedad_ciclo__producto_variedad')
        item['Variedad'] = item.pop('producto_variedad_ciclo__producto_variedad__descripcion')
        item['Productor'] = item.pop('producto_variedad_ciclo__producto_variedad__producto__productor__nombre_fantasia')
        item['Producto'] = item.pop('producto_variedad_ciclo__producto_variedad__producto__titulo')
        item['Cantidad'] = item.pop('cantidad__sum')
        item['Costo Produccion'] = producto_ciclo.costo_produccion
        item['Costo Transporte'] = producto_ciclo.costo_transporte
        item['Costo Financiero'] = producto_ciclo.costo_financiero
        item['Costo Postproceso'] = producto_ciclo.costo_postproceso
        item['A Nodos'] = producto_ciclo.aporte_nodo
        item['Logistica'] = producto_ciclo.aporte_logistica
        item['A la red'] = producto_ciclo.aporte_central
        item['A depositos'] = producto_ciclo.aporte_deposito
        item['Precio final'] = producto_ciclo.precio
        item['Importe Total'] = producto_ciclo.precio * item['Cantidad']
    return items_agrupados
