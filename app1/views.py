from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.conf import settings
from string import ascii_uppercase
from django.http import JsonResponse
import json
from django.utils import timezone
import os

# Vista personalizada para errores CSRF
def csrf_failure(request, reason=""):
    # Renderiza una página de error cuando ocurre un fallo de verificación CSRF
    return render(request, 'csrf_error.html', {'reason': reason})

# Vista de login
def login_view(request):
    if request.method == "POST":
        # Obtiene usuario y contraseña desde el formulario
        username = request.POST['username']
        password = request.POST['password']
        
        # Autentica al usuario con Django
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Si las credenciales son correctas, inicia sesión y redirige a landing
            login(request, user)
            return redirect('landing')  
        else:
            # Si son inválidas, recarga el formulario con un mensaje de error
            return render(request, 'login.html', {'error': 'Credenciales inválidas'})
    
    # Si es GET, simplemente muestra el formulario de login
    return render(request, 'login.html') 

# Vista principal luego del login (requiere estar autenticado)
@login_required
def landing_view(request):
    return render(request, 'landing.html')

# Vista de categorías, muestra todas las opciones de modelos
def categorias_view(request):
    return render(request, 'categorias.html')

# Cierra sesión del usuario y redirige a la página de login
def logout_view(request):
    logout(request)  
    return redirect('login')  

# ----------------------------
# Sección de vistas de modelos de zapatos
# ----------------------------

# Datos comunes de colores y tallas disponibles
COLORES = ['Negro', 'Gris', 'Azul', 'Verde', 'Amarillo']
TALLAS = [36, 37, 38, 39, 40, 41, 42, 43]

def categorias_view(request):
    categorias = [
        {"nombre": "Apache Hombre", "imagen": "images/apacheH1.png", "url": "apache_hombre"},
        {"nombre": "Apolo Hombre", "imagen": "images/apoloH1.png", "url": "apolo_hombre"},
        {"nombre": "Amaka Hombre", "imagen": "images/amakaH1.png", "url": "amaka_hombre"},
        {"nombre": "Nautico Hombre", "imagen": "images/nauticoH1.png", "url": "nautico_hombre"},
        {"nombre": "Bota Hombre", "imagen": "images/botaH1.png", "url": "bota_hombre"},
        {"nombre": "Casual Hombre", "imagen": "images/casualH1.png", "url": "casual_hombre"},
        {"nombre": "Apache Mujer", "imagen": "images/apacheM1.png", "url": "apache_mujer"},
        {"nombre": "Bota Mujer", "imagen": "images/botaM1.png", "url": "bota_mujer"},
    ]
    return render(request, 'categorias.html', {"categorias": categorias})

# Vista genérica que renderiza los modelos de zapatos según el nombre y sexo
# Vista genérica para modelos
def categoria_view(request, nombre_modelo, sexo_abreviado):
    sexo = 'Hombre' if sexo_abreviado == 'H' else 'Mujer'
    sufijo = 'H' if sexo_abreviado == 'H' else 'M'

    # Lista de zapatos con nombre e imagen
    zapatos = [
        {"nombre": f"{nombre_modelo} {sexo}", "imagen": f"images/{nombre_modelo}{sufijo}{i}.png"}
        for i in range(1, 6)
    ]

    # Letras para distinguir cada zapato visualmente (A, B, C, ...)
    letras = list(ascii_uppercase[:len(zapatos)])  # ['A', 'B', 'C', 'D', 'E']

    return render(request, f"categories/{nombre_modelo.lower()}_{sexo.lower()}.html", {
        "zapatos_con_letras": zip(zapatos, letras),
        "colores": COLORES,
        "tallas": TALLAS,
        "sexo": sexo
    })
# ----------------------------
# Vistas específicas que llaman la función genérica con los parámetros adecuados
# ----------------------------

# Zapatos para hombre
def apache_hombre_view(request):
    return categoria_view(request, "Apache", "H")

def apolo_hombre_view(request):
    return categoria_view(request, "Apolo", "H")

def amaka_hombre_view(request):
    return categoria_view(request, "Amaka", "H")

def nautico_hombre_view(request):
    return categoria_view(request, "Nautico", "H")

def bota_hombre_view(request):
    return categoria_view(request, "Bota", "H")

def casual_hombre_view(request):
    return categoria_view(request, "Casual", "H")

# Zapatos para mujer
def apache_mujer_view(request):
    return categoria_view(request, "Apache", "M")

def bota_mujer_view(request):
    return categoria_view(request, "Bota", "M")


def ver_pedidos(request):
    # Recuperamos los datos del pedido de la sesión
    pedido = request.session.get('pedido', {})
    return render(request, 'ver_pedidos.html', {'pedido': pedido})




def agregar_pedido(request):
    if request.method == 'POST':
        modelo = request.POST.get('modelo')
        color = request.POST.get('color')
        talla = request.POST.get('talla')
        sexo = request.POST.get('sexo')
        imagen = request.POST.get('imagen')
        letra = request.POST.get("letra", "").upper()  # Nueva letra A, B, etc.

        letra_sexo = sexo[0].upper()
        
        # Base del ID: ej. AP38H_A
        clave_base = f"{modelo[:2].upper()}{talla}{color[0].upper()}{letra_sexo}{letra}"
        
        pedido = request.session.get('pedido', {})
        contador = 1

        # Detectar si ya hay un ID similar
        ids_existentes = [pid for pid in pedido.keys() if pid.startswith(clave_base)]
        if ids_existentes:
            numeros = [int(pid[len(clave_base):]) for pid in ids_existentes]
            contador = max(numeros) + 1

        idZapato = f"{clave_base}{str(contador).zfill(3)}"

        # Buscar si ya existe un zapato con la misma combinación exacta (incluyendo letra)
        for pid, item in pedido.items():
            if (
                item['modelo'] == modelo and
                item['color'] == color and
                str(item['talla']) == talla and
                item['sexo'] == letra_sexo and
                item.get('letra', '') == letra
            ):
                pedido[pid]['cantidad'] += 1
                break
        else:
            # Agregar zapato nuevo
            pedido[idZapato] = {
                'modelo': modelo,
                'color': color,
                'talla': talla,
                'sexo': letra_sexo,
                'cantidad': 1,
                'imagen': imagen,
                'letra': letra
            }

        request.session['pedido'] = pedido
        return redirect('ver_pedido')


@login_required
def generar_pedido(request):
    if request.method == 'POST':
        # Obtener los productos del pedido desde la sesión (carrito de compras)
        pedido_data = request.session.get('pedido', {})
        
        if not pedido_data:
            messages.error(request, "No hay productos en el carrito.")
            return redirect('ver_pedido')

        # Crear una nueva orden (solo para estructura, no se guardará aún)
        empleado = request.user  # Asumiendo que el usuario logueado es el empleado
        comentario = request.POST.get('comentario', '') # Obtener comentarios adicionales del formulario

        # Guardar el comentario en la sesión
        request.session['comentario'] = comentario 

        # Preparar los datos para el JSON
        orden_data = {
            'empleado': empleado.username,
            'fecha_creacion': timezone.now().isoformat(),
            'estado': 'PENDIENTE',
            'observaciones': comentario,
            'detalles': []
        }

        # Preparar los detalles del pedido sin hacer queries
        for producto_id, producto in pedido_data.items():
            # Generar los IDs del zapato secuenciales
            zapato_ids = []
            for i in range(1, producto['cantidad'] + 1):
                # Generamos el zapato_id secuencial, añadiendo ceros a la izquierda si es necesario
                zapato_ids.append(f"{producto_id[:8]}{str(i).zfill(3)}")  # Ejemplo: AP36NHB001

            # Unir los zapato_id en una cadena separada por comas
            zapato_id_secuenciales = ",".join(zapato_ids)

            # Crear el detalle para este producto
            detalle = {
                'zapato_id': zapato_id_secuenciales,  # Usamos los IDs secuenciales
                'modelo': producto['modelo'],
                'talla': producto['talla'],
                'sexo': producto['sexo'],
                'color': producto['color'],
                'cantidad': producto['cantidad'],
                'imagen': producto.get('imagen', '')
            }

            # Añadimos el detalle al orden
            orden_data['detalles'].append(detalle)

        # Define la ruta donde guardar el archivo JSON
        archivos_pedidos_dir = os.path.join(settings.MEDIA_ROOT, 'archivos_pedidos')
        
        # Crea la carpeta 'archivos_pedidos' si no existe
        if not os.path.exists(archivos_pedidos_dir):
            os.makedirs(archivos_pedidos_dir)

        # Define el nombre del archivo JSON con la fecha de creación para hacerlo único
        file_name = f"pedido_{timezone.now().strftime('%Y%m%d%H%M%S')}.json"
        file_path = os.path.join(archivos_pedidos_dir, file_name)

        # Generar el archivo JSON con los datos de la orden
        with open(file_path, 'w') as archivo:
            json.dump(orden_data, archivo, indent=4)
        
        # Borrar el pedido de la sesión
        if 'pedido' in request.session:
            del request.session['pedido']

        # Mostrar mensaje de éxito
        messages.success(request, f"El pedido se ha generado exitosamente en formato JSON. Puedes verificarlo en: {file_path}")

        # Redirigir al usuario a la vista de pedidos
        return redirect('ver_pedido')
    
    # Si no es un POST, redirigir al carrito
    return redirect('ver_pedido')




def eliminar_pedido(request):
    if request.method == 'POST':
        producto_id = request.POST.get('producto_id')

        # Recuperamos el pedido actual
        pedido = request.session.get('pedido', {})

        # Si hay un pedido en la sesión
        if producto_id in pedido:
            del pedido[producto_id]  # Eliminar el producto por su ID

            # Actualizamos el pedido en la sesión
            request.session['pedido'] = pedido

            # Mensaje de éxito
            messages.success(request, 'Producto eliminado del carrito.')

        return redirect('ver_pedido')  # Redirigimos a la vista de pedidos

    return redirect('landing')  # Si no es un POST, redirigimos a landing

def eliminar_todo_pedido(request):
    if request.method == 'POST':
        # Borramos todo el pedido de la sesión
        if 'pedido' in request.session:
            del request.session['pedido']
            messages.success(request, 'Pedido eliminado con éxito.')
        else:
            messages.warning(request, 'No hay pedido que eliminar.')

        return redirect('ver_pedido')  # Redirigir a la vista de ver pedidos o donde prefieras

    return redirect('landing')  # Redirige a una página por defecto si no es un POST

def actualizar_pedido(request):
    if request.method == 'POST':
        producto_id = request.POST.get('producto_id')
        action = request.POST.get('action')

        # Obtener el carrito desde la sesión
        pedido = request.session.get('pedido', {})

        if producto_id in pedido:
            if action == 'increment':
                pedido[producto_id]['cantidad'] += 1
            elif action == 'decrement' and pedido[producto_id]['cantidad'] > 1:
                pedido[producto_id]['cantidad'] -= 1

        # Guardar el carrito actualizado en la sesión
        request.session['pedido'] = pedido

    return redirect('ver_pedido')



def generar_id_unico(modelo, color, talla, sexo, contador):
    color_inicial = color[0].upper()  # Obtener la inicial del color
    sexo_letra = sexo.upper()  # Obtener la letra del sexo
    id_unico = f"{modelo[:2].upper()}{talla}{color_inicial}{sexo_letra}{str(contador).zfill(3)}"
    return id_unico