from django.urls import path
from .views import login_view, landing_view

urlpatterns = [
    path('', login_view, name='login'),  # Ruta para login
    path('landing/', landing_view, name='landing'),  # Ruta para landing
]
