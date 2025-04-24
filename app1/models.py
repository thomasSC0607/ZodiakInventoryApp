from django.db import models

# Create your models here.

class Zapato(models.Model):
    GENERO_CHOICES = [
        ('H', 'Hombre'),
        ('M', 'Mujer'),
    ]
    TALLAS_CHOICES = [
        ('34', '34'),
        ('35', '35'),
        ('36', '36'),
        ('37', '37'),
        ('38', '38'),
        ('39', '39'),
        ('40', '40'),
        ('41', '41'),
        ('42', '42'),
        ('43', '43'),
        ('44', '44'),
        ('45', '45'),
    ]
    MODELO_CHOICES = [
        ('Apache', 'Apache'),
        ('Apolo', 'Apolo'),
        ('Amaka', 'Amaka'),
        ('Nautico', 'Nautico'),
        ('Bota', 'Bota'),
        ('Casual', 'Casual'),
        ('Sport', 'Sport'),
    ]
    COLOR_CHOICES = [
        ('Rojo', 'Rojo'),
        ('Azul', 'Azul'),
        ('Verde', 'Verde'),
        ('Amarillo', 'Amarillo'),
    ]
    referencia = models.CharField(max_length=20)
    # El modelo es lo mismo que la categoría del zapato
    modelo = models.CharField(max_length=10, choices=MODELO_CHOICES) # En el formulario se puede manejar a través de opciones
    talla = models.CharField(max_length=2, choices=TALLAS_CHOICES)
    sexo = models.CharField(max_length=1, choices=GENERO_CHOICES)
    color = models.CharField(max_length=10, choices=COLOR_CHOICES)
    requerimientos = models.TextField()
    observaciones = models.TextField(default='Sin observaciones', null=True, blank=True) # El campo observaciones es opcional    

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=15)
    correo = models.EmailField()
    
class Orden(models.Model):
    ESTADO_CHOICES = [
        ('P', 'Pendiente'),
        ('C', 'Completada'),
        ('A', 'Anulada'),
    ]

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_terminacion = models.DateTimeField(null=True, blank=True) # La fecha de terminación es opcional
    estado = models.CharField(max_length=1, choices=ESTADO_CHOICES, default='P') # El estado por defecto es pendiente
    observaciones = models.TextField(default='Sin observaciones', null=True, blank=True) # El campo observaciones es opcional
    zapato = models.ForeignKey(Zapato, on_delete=models.CASCADE) # Relación uno a muchos con la tabla Zapato
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE) # Relación uno a muchos con la tabla Cliente
