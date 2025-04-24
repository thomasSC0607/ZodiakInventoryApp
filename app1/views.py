from django.shortcuts import render, redirect
from .forms import ZapatoForm
from .models import Zapato
from django.http import HttpResponseRedirect
from django.contrib import messages
import qrcode
import os

def generar_qr(zapato):
    """
    Genera un código QR para un zapato y devuelve la imagen.
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data({
        'referencia': zapato.referencia,
        'modelo': zapato.modelo,
        'talla': zapato.talla,
        'sexo': zapato.sexo,
        'color': zapato.color,
        'requerimientos': zapato.requerimientos,
        'observaciones': zapato.observaciones,
    })
    qr.make(fit=True)
    return qr.make_image(fill_color="black", back_color="white")

def guardar_qr(zapato, img):
    """
    Guarda la imagen del QR en un directorio específico.
    """
    qr_directory = 'qr_codes/'  # Directorio donde se guardarán los QR
    os.makedirs(qr_directory, exist_ok=True)  # Crea el directorio si no existe
    qr_path = os.path.join(qr_directory, f"zapato_{zapato.id}.png")
    img.save(qr_path)
    return qr_path

def crear_zapato(request):
    if request.method == 'POST':
        form = ZapatoForm(request.POST)
        if form.is_valid():
            # Obtén los datos del formulario sin guardar en la base de datos
            zapato_data = form.cleaned_data

            try:
                # Crea un objeto temporal de tipo Zapato para generar el QR
                zapato = Zapato(**zapato_data)
                img = generar_qr(zapato)  # Genera el QR
                qr_path = guardar_qr(zapato, img)  # Guarda el QR en el sistema de archivos

                # Mensaje de éxito con la ruta del QR generado
                messages.success(request, f"Código QR generado exitosamente: {qr_path}")
            except Exception as e:
                # Manejo de errores
                messages.error(request, f"Error al generar el QR: {e}")

            return redirect('crear_zapato')  # Redirige después de generar el QR
    else:
        form = ZapatoForm()
    return render(request, 'app1/home.html', {'form': form})

