from django.urls import path

from . import views

urlpatterns = [
    # path('<int:ciclo_id>/', views.productos_x_ciclo(), name='Productos x Ciclo'),
    path('', views.catalogo, name='Catálogo'),
    path('catalogo', views.catalogo, name='Catálogo'),
    path('catalogo_pdf', views.catalogo_pdf, name="Catálogo-pdf"),
    path('catalogo_interno', views.catalogo_interno, name='Catálogo Interno'),
    path('productores', views.productores, name='Productores'),
    path('remitos_nodos', views.remitos_nodos, name='Remitos Nodos'),
    path('remitos_productores', views.remitos_productores, name='Remitos Productores'),
    path('resumen_pedidos', views.resumen_pedidos, name='Resumen Pedidos'),
    path('resumen_post_proceso', views.resumen_post_proceso, name='Resumen Postproceso'),
]
