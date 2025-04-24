from django.contrib import admin
from .models import Zapato, Cliente, Orden

# Register your models here. Para administrar los datos de la base de datos desde el panel de administración de Django.
admin.site.register(Zapato)
admin.site.register(Cliente)
admin.site.register(Orden)

# Superuser credentials:
# Username: thomas
# Password: zodiak