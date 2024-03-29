from django.urls import path

from . import views

urlpatterns = [
    path('', views.catalogo, name='Catálogo'),
    path('catalogo', views.catalogo, name='Catálogo'),
    path('catalogo_pdf', views.catalogo_pdf, name="Catálogo-pdf"),
    path('catalogo_interno', views.catalogo_interno, name='Catálogo Interno'),
    path('remitos_nodos', views.remitos_nodos, name='Remitos Nodos'),
    path('remitos_productores', views.remitos_productores, name='Remitos Productores'),
    path('resumen_pedidos', views.resumen_pedidos, name='Resumen Pedidos'),
    path('resumen_post_proceso', views.resumen_post_proceso, name='Resumen Postproceso'),
    path('panel', views.panel_contacto, name='Panel'),
    path('productores', views.ProductoresLista.as_view(), name='productores-lista'),
    path('nodos/', views.NodosLista.as_view(), name='nodo-lista'),

    path('pedidos/', views.PedidosLista.as_view(), name='pedido-lista'),
    path('pedidos/resumen/<int:id_pedido>/', views.resumen_pedido, name='pedido-resumen'),
    path('pedidos/planilla/<int:id_nodo>/', views.pedidos_planilla, name='pedido-planilla'),
    path('pedidos/crear/<int:id_nodo>/', views.PedidosCrear.as_view(), name='pedido-crear'),
    path('pedidos/modificar/<int:pk>/<int:id_nodo>/', views.PedidosModificar.as_view(), name='pedido-modificar'),
    path('pedidos/eliminar/<int:pk>/', views.PedidosEliminar.as_view(), name='pedido-eliminar'),
    path('pedidos/corregir', views.pedidos_corregir, name='pedido-corregir')
]
