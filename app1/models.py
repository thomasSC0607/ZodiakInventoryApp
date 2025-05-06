
# app1/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class Empleado(AbstractUser):
    cedula = models.CharField(max_length=15, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
