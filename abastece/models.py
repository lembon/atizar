from django.db import models

class Domicilio(models.Model):
    pais = models.CharField(max_length=200, default="Argentina")
    provincia = models.CharField(max_length=100, default="Catamarca")
    localidad = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    codigo_postal = models.CharField(max_length=100)

class Contacto(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=100, blank=True)
    domicilio = models.ForeignKey(Domicilio, models.SET_NULL, null=True, blank=True)
    email = models.EmailField(blank=True)
    descripcion = models.TextField(blank=True)
    web = models.URLField(blank=True)
    
class Nodo(models.Model):
    referentes = models.ManyToManyField(Contacto)
    domicilio = models.ForeignKey(Domicilio, models.PROTECT) #Domicilio de funcionamiento del nodo
    domicilio_recepcion = models.ForeignKey(Domicilio, models.SET_NULL, null = True, blank = True, related_name="domicilio_recepcion")
    
class Miembro(models.Model):
    contacto = models.ForeignKey(Contacto, models.CASCADE)
    nodo = models.ForeignKey(Nodo, models.CASCADE)

class Producto(models.Model):
    productor = models.ForeignKey(Contacto, models.CASCADE)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    envase = models.CharField(max_length=200)
    cantidad = models.IntegerField() #Ver de agregar MinValueValidator
    unidad = models.CharField(max_length = 100) ## VER de poner choice
    costo_produccion = models.DecimalField(max_digits=8, decimal_places=2)
    costo_transporte = models.DecimalField(max_digits=8, decimal_places=2)
    costo_financiero = models.DecimalField(max_digits=8, decimal_places=2)
    
class ProductoVariedad(models.Model):
    producto = models.ForeignKey(Producto, models.CASCADE)
    descripcion = models.CharField(max_length=200)
    disponible = models.IntegerField() #Ver de agregar MinValueValidator    
    
class ImagenProducto(models.Model):
    producto=models.ForeignKey(Producto, models.CASCADE)
    imagen=models.ImageField
    # https://stackoverflow.com/a/537966
    
class Ciclo(models.Model):
    inicio = models.DateTimeField('inicio pedidos')    
    cierre = models.DateTimeField('cierre pedidos')
    
class ProductoCiclo(models.Model):   ###O va ProductoVariedad?
    ciclo = models.ForeignKey(Ciclo, models.CASCADE)
    producto = models.ForeignKey(Producto, models.CASCADE)
    precio = models.DecimalField(max_digits=8, decimal_places=2)

class Pedido(models.Model):
    ciclo = models.ForeignKey(Ciclo, models.CASCADE)
    timestamp = models.DateTimeField('fecha y hora')
    miembro = models.ForeignKey(Miembro, models.CASCADE)

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, models.CASCADE)
    producto_variedad = models.ForeignKey(ProductoVariedad, models.CASCADE)
    cantidad = models.IntegerField
