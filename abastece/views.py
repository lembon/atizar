from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from weasyprint import HTML

from abastece.logic import resumen
from abastece.models import Ciclo, ProductoVariedadCiclo


def catalogo_interno(request):
    ciclo = Ciclo.objects.latest("inicio")
    variedades_en_ciclo = ProductoVariedadCiclo.objects.filter(ciclo=ciclo)
    context = {'variedades_en_ciclo': variedades_en_ciclo, }
    return render(request, 'abastece/catalogo_interno.html', context)


def catalogo(request):
    ciclo = Ciclo.objects.latest("inicio")
    variedades_en_ciclo = ProductoVariedadCiclo.objects.filter(ciclo=ciclo)
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
    response["Content-Disposition"] = "inline; report.pdf"
    html = HTML(string=html_string)
    html.write_pdf(response, )
    return response


def remitos_productores(request):
    ciclo = Ciclo.objects.latest("inicio")
    context = {'remitos': resumen.remitos_productores(ciclo)}
    html_string = render_to_string('abastece/remitos_productores.html', context)
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "inline; report.pdf"
    html = HTML(string=html_string)
    html.write_pdf(response, )
    return response


def resumen_post_proceso(request):
    ciclo = Ciclo.objects.latest("inicio")
    context = {'resumen': resumen.resumen_post_proceso(ciclo)}
    html_string = render_to_string('abastece/resumen_post_proceso.html', context)
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "inline; report.pdf"
    html = HTML(string=html_string)
    html.write_pdf(response, )
    return response
