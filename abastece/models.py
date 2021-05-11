from decimal import Decimal

from django.conf import settings
from django.db import models
from django.utils.html import mark_safe


def get_upload_path(instance, filename):
    return 'contactos/{}/{}'.format(instance.upload_path(), filename)


class Domicilio(models.Model):
    pais = models.CharField(max_length=200, default="Argentina")
    provincia = models.CharField(max_length=100, default="Catamarca")
    localidad = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    codigo_postal = models.CharField(max_length=100)

    def __str__(self):
        return "{}, {} CP {}, {}, {}".format(self.direccion, self.localidad, self.codigo_postal, self.provincia,
                                             self.pais)


class Contacto(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    nombre_fantasia = models.CharField(max_length=100, blank=True)
    telefono = models.CharField(max_length=100, blank=True)
    domicilio = models.ForeignKey(Domicilio, models.SET_NULL, null=True, blank=True)
    email = models.EmailField(blank=True)
    descripcion = models.TextField(blank=True)
    web = models.URLField(blank=True)

    def __str__(self):
        return self.nombre_fantasia or "{} {}".format(self.nombre, self.apellido)

    def get_web_name(self):
        return self.__str__().lower().replace(' ', '_')

    def is_productor(self):
        return bool(self.productos.count())
    is_productor.boolean = True
    is_productor.short_description = '¿Es Productor?'


class ImagenContacto(models.Model):
    contacto = models.ForeignKey(Contacto, models.CASCADE)
    imagen = models.ImageField(upload_to=get_upload_path)

    def image_tag(self):
        return mark_safe('<img src="%s%s" width="150" height="150" />' % (settings.MEDIA_URL, self.imagen))
    image_tag.short_description = 'Imagen'

    def upload_path(self):
        return self.contacto.get_web_name()


class Nodo(models.Model):
    nombre = models.CharField(max_length=200)
    domicilio = models.ForeignKey(Domicilio, models.PROTECT)  # Domicilio de funcionamiento del nodo
    domicilio_recepcion = models.ForeignKey(Domicilio,
                                            models.SET_NULL,
                                            null=True,
                                            blank=True,
                                            related_name="domicilio_recepcion",
                                            help_text="Solo cuando la mercadería se recibe en un domicilio diferente "
                                                      "del de funcionamiento.")

    def __str__(self):
        return self.nombre

    def get_referente(self):
        return self.membresia_set.filter(rol=2).first().contacto

    def get_referente_nombre(self):
        contacto = self.get_referente()
        return contacto.nombre + ' ' + contacto.apellido

    get_referente_nombre.short_description = 'Referente'

    def get_referente_telefono(self):
        contacto = self.get_referente()
        return contacto.telefono

    get_referente_telefono.short_description = 'Teléfono'
class Membresia(models.Model):
    ROLES_NODO = (
        (1, 'comun'),
        (2, 'referente'),
    )

    rol = models.PositiveSmallIntegerField(choices=ROLES_NODO)
    contacto = models.ForeignKey(Contacto, models.CASCADE, related_name='membresias')
    nodo = models.ForeignKey(Nodo, models.CASCADE)


class Producto(models.Model):
    UNIDADES = (
        ("U", 'unidades'),
        ("g", 'gramos'),
        ("kg", 'kilogramos'),
        ("cm3", 'centímetros cúbicos'),
        ("ml", 'mililitros'),
        ("l", 'litros'),
        ("m", 'metros')
    )
    productor = models.ForeignKey(Contacto, models.CASCADE, related_name='productos')
    titulo = models.CharField(max_length=200, unique=True)
    descripcion = models.TextField(blank=True)
    envase = models.CharField(max_length=200, blank=True)
    cantidad = models.IntegerField()  # Ver de agregar MinValueValidator
    unidad = models.CharField(max_length=100, choices=UNIDADES)  # VER de poner choice
    costo_produccion = models.DecimalField(max_digits=8, decimal_places=2)
    costo_transporte = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    costo_financiero = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    costo_postproceso = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return self.titulo

    def get_descripcion_corta(self):
        return self.descripcion.split('\n')[0]

    get_descripcion_corta.short_description = 'Detalle'


class ProductoVariedad(models.Model):
    producto = models.ForeignKey(Producto, models.CASCADE)
    descripcion = models.CharField(max_length=200)
    disponible = models.IntegerField()  # Ver de agregar MinValueValidator

    def __str__(self):
        return self.descripcion

    def en_proximo_ciclo(self):
        proximo_ciclo = Ciclo.objects.latest("inicio")
        return ProductoVariedadCiclo.objects.filter(ciclo=proximo_ciclo, producto_variedad=self).exists()

    en_proximo_ciclo.boolean = True
    en_proximo_ciclo.short_description = '¿En próximo ciclo?'


class ImagenProducto(models.Model):
    producto = models.ForeignKey(Producto, models.CASCADE, related_name='images')
    imagen = models.ImageField(upload_to=get_upload_path)

    def image_tag(self):
        return mark_safe('<img src="%s%s" width="150" height="150" />' % (settings.MEDIA_URL, self.imagen))

    image_tag.short_description = 'Imagen'

    def upload_path(self):
        return self.producto.productor.get_web_name()


class Ciclo(models.Model):
    inicio = models.DateTimeField('inicio pedidos')
    cierre = models.DateTimeField('cierre pedidos')
    aporte_deposito = models.FloatField(default=0)  # Ver de agregar Validators
    aporte_central = models.FloatField(default=0)
    aporte_nodo = models.FloatField(default=0)
    aporte_logistica = models.FloatField(default=0)
    productos = models.ManyToManyField(Producto, related_name='ciclos', through='ProductoCiclo')
    variedades = models.ManyToManyField(ProductoVariedad, related_name='ciclos', through='ProductoVariedadCiclo')

    def __str__(self):
        return "Del {} al {}".format(self.inicio.date(), self.cierre.date())

class ProductoCiclo(models.Model):
    ciclo = models.ForeignKey(Ciclo, models.CASCADE)
    producto = models.ForeignKey(Producto, models.CASCADE)
    costo_produccion = models.DecimalField(max_digits=8, decimal_places=2)
    costo_transporte = models.DecimalField(max_digits=8, decimal_places=2)
    costo_financiero = models.DecimalField(max_digits=8, decimal_places=2)
    costo_postproceso = models.DecimalField(max_digits=8, decimal_places=2)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    """ HAcer un método precio_sugerido que sea el resultante de tod el cálculo y setearlo como default al precio. 
    Y que el precio no pueda variar más de $x con respecto a eso"""

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['ciclo', 'producto'], name='unico producto por ciclo')
        ]

    def save(self, *args, **kwargs):
        if not self.precio:
            self.costo_produccion = self.producto.costo_produccion
            self.costo_transporte = self.producto.costo_transporte
            self.costo_financiero = self.producto.costo_financiero
            self.costo_postproceso = self.producto.costo_postproceso
            self.precio = self.precio_sugerido()
        super(ProductoCiclo, self).save(*args, **kwargs)

    def precio_sugerido(self):
        costos = self.costo_produccion + self.costo_transporte + self.costo_financiero + self.costo_postproceso
        aportes = Decimal(
            self.ciclo.aporte_deposito + self.ciclo.aporte_central + self.ciclo.aporte_nodo + self.ciclo.aporte_logistica)
        return costos + costos * aportes / 100

    def __str__(self):
        return "{} - {}".format(self.producto.productor, self.producto.titulo)


class ProductoVariedadCiclo(models.Model):
    ciclo = models.ForeignKey(Ciclo, models.CASCADE)
    producto_variedad = models.ForeignKey(ProductoVariedad, models.CASCADE)
    disponible = models.IntegerField()  # Ver de agregar MinValueValidator

    def save(self, *args, **kwargs):
        self.disponible = self.producto_variedad.disponible
        super(ProductoVariedadCiclo, self).save(*args, **kwargs)

    def producto_ciclo(self):
        return ProductoCiclo.objects.get(ciclo=self.ciclo, producto=self.producto_variedad.producto)

class Pedido(models.Model):
    timestamp = models.DateTimeField('fecha y hora')  # Hacer Editable = False
    consumidor = models.ForeignKey(Membresia, models.CASCADE)


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, models.CASCADE)
    producto_variedad_ciclo = models.ForeignKey(ProductoVariedadCiclo, models.CASCADE)
    cantidad = models.IntegerField
