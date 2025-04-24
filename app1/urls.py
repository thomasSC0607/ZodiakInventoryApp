from django.urls import path
from . import views

urlpatterns = [
    path('', views.crear_zapato, name='crear_zapato'),
]