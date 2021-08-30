import csv

from django.db import transaction
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from weasyprint import HTML

from abastece.forms import ItemPedidoFormset
from abastece.logic import resumen
from abastece.models import Ciclo, ProductoVariedadCiclo, Contacto, Pedido, Nodo, ItemPedido, Membresia


def catalogo_interno(request):
    ciclo = Ciclo.objects.latest("inicio")
    variedades_en_ciclo = ProductoVariedadCiclo.objects.filter(ciclo=ciclo)
    context = {'variedades_en_ciclo': variedades_en_ciclo, }
    return render(request, 'abastece/catalogo_interno.html', context)


def catalogo(request):
    ciclo = Ciclo.objects.latest("inicio")
    variedades_en_ciclo = ProductoVariedadCiclo.objects.filter(ciclo=ciclo).order_by(
        'producto_variedad__producto__productor', 'producto_variedad__producto', 'producto_variedad__id')
    context = {'variedades_en_ciclo': variedades_en_ciclo, }
    return render(request, 'abastece/catalogo.html', context)


def catalogo_pdf(request):
    ciclo = Ciclo.objects.latest("inicio")
    variedades_en_ciclo = ProductoVariedadCiclo.objects.filter(ciclo=ciclo)
    context = {'variedades_en_ciclo': variedades_en_ciclo, }
    html_string = render_to_string('abastece/catalogo_pdf.html', context)
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "inline; report.pdf"
    html = HTML(string=html_string)
    html.write_pdf(response, )
    return response


def remitos_nodos(request):
    ciclo = Ciclo.objects.latest("inicio")
    context = {'remitos': resumen.remitos_nodos(ciclo)}
    html_string = render_to_string('abastece/remitos_nodos.html', context)
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "inline; remitos_nodos.pdf"
    html = HTML(string=html_string)
    html.write_pdf(response, )
    return response


def remitos_productores(request):
    ciclo = Ciclo.objects.latest("inicio")
    context = {'remitos': resumen.remitos_productores(ciclo)}
    html_string = render_to_string('abastece/remitos_productores.html', context)
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "inline; remitos_productores.pdf"
    html = HTML(string=html_string)
    html.write_pdf(response, )
    return response


def resumen_post_proceso(request):
    ciclo = Ciclo.objects.latest("inicio")
    context = {'resumen': resumen.resumen_post_proceso(ciclo)}
    html_string = render_to_string('abastece/resumen_post_proceso.html', context)
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "inline; resumen_post_proceso.pdf"
    html = HTML(string=html_string)
    html.write_pdf(response, )
    return response


def resumen_pedidos(request):
    ciclo = Ciclo.objects.latest("inicio")
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="resumen_pedidos.csv"'
    items_agrupados = resumen.resumen_pedidos(ciclo)
    writer = csv.DictWriter(response, fieldnames=items_agrupados[0].keys())
    writer.writeheader()
    writer.writerows(items_agrupados)
    actual_total_lines = {k: v.format(filas=len(items_agrupados) + 1) for k, v in resumen.TOTALES_RESUMEN.items()}
    writer.writerow(actual_total_lines)
    return response


def ProductoresLista(request):
    productores = Contacto.objects.annotate(num_productos=Count('productos')).filter(num_productos__gt=0).order_by(
        'nombre_fantasia')
    context = {'productores': productores, }
    return render(request, 'abastece/productores.html', context)


@login_required
def panel_contacto(request):
    return render(request, 'abastece/panel-contacto.html', )


@login_required
def pedidos_planilla(request):
    ciclo = Ciclo.objects.latest("inicio")
    nodo = request.user.contacto.get_nodos_referente()[0]
    pedidos = Pedido.objects.filter(consumidor__nodo=nodo, timestamp__range=(ciclo.inicio, ciclo.cierre))
    items = ItemPedido.objects.filter(pedido__in=pedidos)
    productos_variedad_ciclos = ProductoVariedadCiclo.objects.filter(itempedido__in=items). \
        distinct(). \
        order_by('producto_variedad')
    planilla = []
    fila_encabezado = pedidos
    fila_totales = {'columnas': []}
    for producto_var_cic in productos_variedad_ciclos:
        fila = {'producto': producto_var_cic,
                'columnas': []}
        for pedido in pedidos:
            try:
                fila['columnas'].append(items.get(pedido=pedido, producto_variedad_ciclo=producto_var_cic).cantidad)
            except ItemPedido.DoesNotExist:
                fila['columnas'].append(0)
        fila['cantidad_total'] = sum(fila['columnas'])
        fila['importe_nodo'] = fila['cantidad_total'] * producto_var_cic.producto_ciclo.aporte_nodo()
        fila['importe_total'] = fila['cantidad_total'] * producto_var_cic.producto_ciclo.precio
        planilla.append(fila)

    fila_totales['columnas'].extend([pedido.importe for pedido in pedidos])
    fila_totales['importe_nodo'] = sum([fila['importe_nodo'] for fila in planilla])
    fila_totales['importe_total'] = sum([fila['importe_total'] for fila in planilla])

    context = {'encabezado': fila_encabezado,
               'filas': planilla,
               'totales': fila_totales}

    return render(request, 'abastece/pedido_planilla.html', context)


class PedidosCrear(LoginRequiredMixin, CreateView):
    model = Pedido
    fields = ['nombre']
    success_url = reverse_lazy('pedido-planilla')

    def get_context_data(self, **kwargs):
        data = super(PedidosCrear, self).get_context_data(**kwargs)
        if self.request.POST:
            data['items_pedido'] = ItemPedidoFormset(self.request.POST)
        else:
            data['items_pedido'] = ItemPedidoFormset()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        items_pedido = context['items_pedido']
        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.consumidor = Membresia.objects.filter(contacto=self.request.user.contacto, rol=2).first()
            self.object.save()

            if items_pedido.is_valid():
                items_pedido.instance = self.object
                items_pedido.save()
        return super(PedidosCrear, self).form_valid(form)


class PedidosModificar(LoginRequiredMixin, UpdateView):
    model = Pedido
    fields = ['nombre']
    success_url = reverse_lazy('pedido-planilla')

    def get_context_data(self, **kwargs):
        data = super(PedidosModificar, self).get_context_data(**kwargs)
        if self.request.POST:
            data['items_pedido'] = ItemPedidoFormset(self.request.POST, instance=self.object)
        else:
            data['items_pedido'] = ItemPedidoFormset(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        items_pedido = context['items_pedido']
        with transaction.atomic():
            self.object = form.save()

            if items_pedido.is_valid():
                items_pedido.instance = self.object
                items_pedido.save()
        return super(PedidosModificar, self).form_valid(form)


class PedidosEliminar(LoginRequiredMixin, DeleteView):
    model = Pedido
    template_name_suffix = '_confirmar_eliminar'
    success_url = reverse_lazy('pedido-planilla')


class NodosLista(ListView):
    model = Nodo


class PedidosLista(LoginRequiredMixin, ListView):
    def get_queryset(self):
        ciclo = Ciclo.objects.latest("inicio")
        nodos = self.request.user.contacto.get_nodos_referente()
        return Pedido.objects.filter(consumidor__nodo__in=nodos, timestamp__range=(ciclo.inicio, ciclo.cierre))
