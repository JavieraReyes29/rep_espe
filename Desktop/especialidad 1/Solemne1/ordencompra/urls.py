from django.urls import path
from ordencompra import views #importará los métodos que generemos en nuestra app
from django.views.decorators.csrf import csrf_exempt
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

ordencompra_urlpatterns = [
    path('order_main/',views.order_main,name="order_main"),
    path('crear_orden_compra/', views.crear_orden_compra, name='crear_orden_compra'),
    path('ver_orden_compra/<int:orden_id>/', views.ver_orden_compra, name='ver_orden_compra'),
    path('eliminar_orden_compra/<int:orden_id>/', views.eliminar_orden_compra, name='eliminar_orden_compra'),
    path('listar_ordenes_compra/', views.listar_ordenes_compra, name='listar_ordenes_compra'),
    path('agregar_item/<int:orden_id>/', views.agregar_item, name='agregar_item'),
    path('eliminar_item/<int:item_id>/', views.eliminar_item, name='eliminar_item'),
]