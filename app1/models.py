
# app1/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class Empleado(AbstractUser):
    cedula = models.CharField(max_length=15, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
class Bodega(models.Model):
    modelo = models.CharField(max_length=100)
    talla = models.IntegerField()
    sexo = models.CharField(max_length=1, choices=[('H', 'Hombre'), ('M', 'Mujer')])
    color_principal = models.CharField(max_length=45)
    categoria = models.CharField(max_length=45)
    cantidad_disponible = models.IntegerField()

    def __str__(self):
        return f"{self.modelo} {self.sexo} T{self.talla} - {self.color_principal} ({self.cantidad_disponible})"
    

class Zapato(models.Model):
    idZapato = models.CharField(max_length=20, primary_key=True, editable=False)
    modelo = models.CharField(max_length=100)
    talla = models.IntegerField()
    sexo = models.CharField(max_length=1, choices=[('H', 'Hombre'), ('M', 'Mujer')])
    color_principal = models.CharField(max_length=45)
    categoria = models.CharField(max_length=45)
    observaciones = models.CharField(max_length=100, blank=True)
    bodega = models.ForeignKey('Bodega', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.idZapato:
            # Ej: APH38_H001
            base_id = f"{self.modelo[:3].upper()}{self.talla}_{self.sexo}"
            # Buscar cuántos zapatos existen ya con ese mismo modelo, talla y sexo
            count = Zapato.objects.filter(
                modelo=self.modelo, talla=self.talla, sexo=self.sexo
            ).count() + 1
            self.idZapato = f"{base_id}{str(count).zfill(3)}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.idZapato
    
    
class Orden(models.Model):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('EN_PROCESO', 'En Proceso'),
        ('FINALIZADO', 'Finalizado'),
    ]
    
    idOrden = models.AutoField(primary_key=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_terminacion = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='PENDIENTE')
    observaciones = models.TextField(blank=True)
    empleado = models.ForeignKey('Empleado', on_delete=models.CASCADE)

    def __str__(self):
        return f"Orden #{self.idOrden} - {self.empleado.username} - {self.estado}"
    
class DetallePedido(models.Model):
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE)
    zapato = models.ForeignKey(Zapato, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    imagen_zapato = models.ImageField(upload_to='pedidos/', blank=True)

    def __str__(self):
        return f"{self.orden.idOrden} - {self.zapato.idZapato} x{self.cantidad}"