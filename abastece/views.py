from django.shortcuts import render

from .models import Ciclo, ProductoVariedadCiclo


def productos_x_ciclo(request):
    ciclo = Ciclo.objects.latest("inicio")
    variedades_en_ciclo = ProductoVariedadCiclo.objects.filter(ciclo=ciclo)
    context = {'variedades_en_ciclo': variedades_en_ciclo, }
    return render(request, 'abastece/productos_x_ciclo.html', context)
