import csv

from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from weasyprint import HTML

from abastece.logic import resumen
from abastece.models import Ciclo, ProductoVariedadCiclo, Contacto


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


def productores(request):
    productores = Contacto.objects.annotate(num_productos=Count('productos')).filter(num_productos__gt=0).order_by(
        'nombre_fantasia')
    context = {'productores': productores, }
    return render(request, 'abastece/productores.html', context)
