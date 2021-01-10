from django.contrib import admin

from .models import Producto, ImagenProducto, Contacto, ImagenContacto, Nodo, Membresia, ProductoVariedad, Ciclo, \
    Domicilio


##  CONTACTO
class ProductoInline(admin.TabularInline):
    model = Producto
    extra = 3


class ImagenContactoInline(admin.StackedInline):
    model = ImagenContacto
    extra = 1


@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['nombre', 'apellido', 'nombre_fantasia', 'descripcion', 'web']}),
        ('Datos de Contacto', {'fields': ['telefono', 'domicilio', 'email'], 'classes': ['collapse']}),
    ]
    inlines = [ProductoInline, ImagenContactoInline]


##

## PRODUCTO

class ProductoVariedadInline(admin.TabularInline):
    model = ProductoVariedad
    extra = 1


class ImagenProductoInline(admin.StackedInline):
    model = ImagenProducto
    extra = 1


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['productor', 'titulo', 'descripcion']}),
        ('Presentación', {'fields': [('envase', 'cantidad', 'unidad')]}),
        ('Costos', {'fields': [('costo_produccion', 'costo_financiero', 'costo_transporte', 'costo_postproceso')]})
    ]
    inlines = [ProductoVariedadInline, ImagenProductoInline]


##

## NODO
class MembresiaInline(admin.StackedInline):
    model = Membresia
    extra = 1


@admin.register(Nodo)
class NodoAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['nombre', 'domicilio', 'domicilio_recepcion']}),
    ]
    inlines = [MembresiaInline]


##

## DOMICILIO
@admin.register(Domicilio)
class DomicilioAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['pais', 'provincia', 'localidad', 'direccion', 'codigo_postal']}),
    ]
##
