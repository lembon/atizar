from django.contrib import admin

from .models import Producto, ImagenProducto, Contacto, ImagenContacto, Nodo, Membresia,\
    ProductoVariedad, Domicilio


class ImagenContactoInline(admin.TabularInline):
    model = ImagenContacto
    extra = 1
    readonly_fields = ('image_tag',)


@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['nombre', 'apellido', 'nombre_fantasia', 'descripcion', 'web']}),
        ('Datos de Contacto', {'fields': ['telefono', 'domicilio', 'email'], }),
    ]
    inlines = [ImagenContactoInline]


class ProductoVariedadInline(admin.TabularInline):
    model = ProductoVariedad
    extra = 1
    min_num = 1


class ImagenProductoInline(admin.TabularInline):
    model = ImagenProducto
    extra = 1
    readonly_fields = ('image_tag',)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['productor', 'titulo', 'descripcion']}),
        ('Presentación', {'fields': [('envase', 'cantidad', 'unidad')]}),
        ('Costos', {'fields': [('costo_produccion', 'costo_financiero', 'costo_transporte', 'costo_postproceso')]})
    ]
    inlines = [ProductoVariedadInline, ImagenProductoInline]


class MembresiaInline(admin.TabularInline):
    model = Membresia
    extra = 1
    fields = ('rol', 'contacto')


@admin.register(Nodo)
class NodoAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['nombre', 'domicilio', 'domicilio_recepcion']}),
    ]
    inlines = [MembresiaInline]


@admin.register(Domicilio)
class DomicilioAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['pais', 'provincia', 'localidad', 'direccion', 'codigo_postal']}),
    ]

    def get_model_perms(self, request):
        """
        Para permitir crear Domicilios a partir de foreign keys de otros modelos, pero ocultarlo del index.
        """
        return {}
##
