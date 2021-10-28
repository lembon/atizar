from django.contrib import admin
from django.forms.models import ModelForm
from django.utils.translation import gettext_lazy as _

from .models import Producto, ImagenProducto, Contacto, ImagenContacto, Nodo, Membresia, \
    ProductoVariedad, Domicilio, Ciclo, ProductoCiclo, ProductoVariedadCiclo, Pedido, ItemPedido


class IsProductorListFilter(admin.SimpleListFilter):
    title = _('participacion')
    parameter_name = 'rol'

    def lookups(self, request, model_admin):
        return (
            ('consumidor', _('Consumidores/as')),
            ('productor', _('Productores/as')),
            ('referente', _('Referentes')),
        )

    def queryset(self, request, queryset):

        if self.value() == 'productor':
            return queryset.filter(productos__isnull=False).distinct()
        elif self.value() == 'consumidor':
            return queryset.filter(membresias__isnull=False).distinct()
        elif self.value() == 'referente':
            return queryset.filter(membresias__rol=2).distinct()


class ImagenContactoInline(admin.TabularInline):
    model = ImagenContacto
    extra = 1
    readonly_fields = ('image_tag',)


@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'telefono', 'domicilio', 'email', 'is_productor')
    list_filter = (IsProductorListFilter, 'domicilio__provincia')
    search_fields = ['apellido', 'descripcion', 'nombre', 'nombre_fantasia', 'productos__titulo']
    fieldsets = [
        (None, {'fields': ['usuario', 'nombre', 'apellido', 'nombre_fantasia', 'descripcion', 'web']}),
        ('Datos de Contacto', {'fields': ['telefono', 'domicilio', 'email'], }),
        ('Otros', {'fields': ['cbu_o_alias', 'notas'], }),
    ]
    inlines = [ImagenContactoInline]


class AlwaysChangedModelForm(ModelForm):
    def has_changed(self):
        # https://stackoverflow.com/a/3734700/1232955
        return True


class ProductoVariedadInline(admin.TabularInline):
    model = ProductoVariedad
    extra = 0
    min_num = 1
    form = AlwaysChangedModelForm


class ImagenProductoInline(admin.TabularInline):
    model = ImagenProducto
    extra = 1
    readonly_fields = ('image_tag',)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('productor', '__str__', 'get_descripcion_corta', 'envase', 'cantidad', 'unidad',)
    list_filter = (
        ('productor', admin.RelatedOnlyFieldListFilter),
    )
    search_fields = ('productor__nombre_fantasia', 'titulo', 'descripcion',)
    fieldsets = [
        (None, {'fields': ['productor', 'titulo', 'descripcion']}),
        ('Presentación', {'fields': [('envase', 'cantidad', 'unidad')]}),
        ('Costos', {'fields': [('costo_produccion', 'costo_financiero', 'costo_transporte', 'costo_postproceso'), ('porcentaje_aporte')]})
    ]
    inlines = [ProductoVariedadInline, ImagenProductoInline]
    ordering = ['productor', 'pk']

@admin.register(ProductoVariedad)
class ProductoVariedadAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_productor', 'producto', 'get_presentacion', '__str__', 'en_proximo_ciclo')
    list_display_links = None
    list_filter = (
        ('producto__productor', admin.RelatedOnlyFieldListFilter),
    )
    search_fields = ('productor__nombre_fantasia', 'producto', 'descripcion',)
    ordering = ('producto__productor', 'id')
    actions = ['agregar_a_ciclo', 'quitar_de_ciclo']

    def get_productor(self, obj):
        return obj.producto.productor

    def get_presentacion(self, obj):
        return obj.producto.presentacion

    get_productor.admin_order_field = 'Productor'  # Allows column order sorting
    get_productor.short_description = 'Productor'  # Renames column head

    def agregar_a_ciclo(self, request, queryset):
        ciclo = Ciclo.objects.latest("inicio")
        productos = Producto.objects.filter(productovariedad__in=queryset).distinct()
        for producto in productos:
            producto_ciclo, creado = ProductoCiclo.objects.get_or_create(producto=producto, ciclo=ciclo)
        for variedad in queryset:
            producto_variedad_ciclo, creado = ProductoVariedadCiclo.objects.get_or_create(producto_variedad=variedad,
                                                                                          ciclo=ciclo)
    agregar_a_ciclo.short_description = "Agregar al próximo ciclo"

    def quitar_de_ciclo(self, request, queryset):
        ciclo = Ciclo.objects.latest("inicio")
        for variedad in queryset:
            ProductoVariedadCiclo.objects.get(producto_variedad=variedad, ciclo=ciclo).delete()

        productos = Producto.objects.filter(productovariedad__in=queryset).distinct()
        for producto in productos:
            if not ProductoVariedadCiclo.objects.filter(producto_variedad__producto=producto, ciclo=ciclo).exists():
                ProductoCiclo.objects.filter(producto=producto, ciclo=ciclo).delete()
    quitar_de_ciclo.short_description = "Quitar del próximo ciclo"

class MembresiaInline(admin.TabularInline):
    model = Membresia
    extra = 1
    fields = ('rol', 'contacto')


@admin.register(Nodo)
class NodoAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'domicilio', 'get_referente_nombre', 'get_referente_telefono', 'mostrar')
    fieldsets = [
        (None, {'fields': ['nombre', 'mostrar', 'domicilio', 'domicilio_recepcion']}),
    ]
    inlines = [MembresiaInline]


@admin.register(Domicilio)
class DomicilioAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['pais', 'provincia', 'localidad', 'direccion', 'codigo_postal']}),
    ]

    def get_model_perms(self, request):
        # Para permitir crear Domicilios a partir de foreign keys de otros modelos, pero ocultarlo del index.
        return {}


@admin.register(Ciclo)
class CicloAdmin(admin.ModelAdmin):
    list_display = ('inicio', 'cierre', 'aporte_deposito', 'aporte_central', 'aporte_nodo', 'aporte_logistica')
    fieldsets = [
        (
        None, {'fields': ['inicio', 'cierre', 'aporte_deposito', 'aporte_central', 'aporte_nodo', 'aporte_logistica']}),
    ]


@admin.register(ProductoCiclo)
class ProductoCicloAdmin(admin.ModelAdmin):
    list_editable = ('precio',)
    list_display = ('__str__', 'precio_sugerido', 'precio')
    list_display_links = None

    def get_queryset(self, request):
        qs = super(ProductoCicloAdmin, self).get_queryset(request)
        ciclos = Ciclo.objects.all()
        if ciclos:
            return qs.filter(ciclo=ciclos.latest("inicio"))
        else:
            return qs


class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 5
    min_num = 1

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "producto_variedad_ciclo":
            kwargs["queryset"] = ProductoVariedadCiclo.objects.filter(ciclo=Ciclo.objects.latest("inicio")).order_by(
                'producto_variedad__producto__productor', 'producto_variedad__pk')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('consumidor','nombre','timestamp','importe')

    def get_queryset(self, request):
        qs = super(PedidoAdmin, self).get_queryset(request)
        ciclos = Ciclo.objects.all()
        if ciclos:
            ciclo = ciclos.latest("inicio")
            return qs.filter(timestamp__range=(ciclo.inicio, ciclo.cierre))
        else:
            return qs

    inlines = [ItemPedidoInline]
