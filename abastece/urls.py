from django.urls import path

from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    # path('<int:ciclo_id>/', views.productos_x_ciclo(), name='Productos x Ciclo'),
    path('', views.productos_x_ciclo, name='Productos x Ciclo'),

]
