from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.conf import settings
from django.utils import timezone
from string import ascii_uppercase
from django.http import JsonResponse
import os
import json

# -----------------------------
# Manejo de errores CSRF
# -----------------------------
def csrf_failure(request, reason=""):
    # Esta vista se muestra cuando ocurre un error de verificación CSRF
    # El error CSRF generalmente ocurre cuando un formulario no tiene un token de seguridad
    return render(request, 'csrf_error.html', {'reason': reason})

# -----------------------------
# Autenticación
# -----------------------------

def login_view(request):
    # Vista que maneja el inicio de sesión del usuario
    if request.method == "POST":
        # Se obtiene el nombre de usuario y la contraseña del formulario
        username = request.POST['username']
        password = request.POST['password']

        # Se intenta autenticar al usuario
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Si la autenticación es exitosa, se inicia sesión con el usuario
            login(request, user)
            # Redirige a la vista principal después de iniciar sesión
            return redirect('landing')
        else:
            # Si la autenticación falla, se muestra un mensaje de error
            return render(request, 'login.html', {'error': 'Credenciales inválidas'})
    
    # Si la solicitud es GET, simplemente se muestra el formulario de inicio de sesión
    return render(request, 'login.html')

def logout_view(request):
    # Esta vista maneja el cierre de sesión del usuario
    logout(request)
    # Redirige al usuario de vuelta a la página de inicio de sesión
    return redirect('login')

@login_required
def landing_view(request):
    # Esta vista es la página principal a la que se accede después de iniciar sesión
    # Sólo los usuarios autenticados pueden acceder a ella
    return render(request, 'landing.html')

# -----------------------------
# Vista de categorías de zapatos
# -----------------------------

def categorias_view(request):
    # Vista que muestra todas las categorías de zapatos
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
    # Retorna una página con las categorías de zapatos
    return render(request, 'categorias.html', {"categorias": categorias})

# -----------------------------
# Vista genérica para mostrar modelos
# -----------------------------

COLORES = ['Negro', 'Gris', 'Azul', 'Verde', 'Amarillo']
TALLAS = [36, 37, 38, 39, 40, 41, 42, 43]

def categoria_view(request, nombre_modelo, sexo_abreviado):
    # Esta es una vista genérica que muestra los modelos de zapatos de una categoría específica
    # 'nombre_modelo' es el nombre del modelo de zapato (por ejemplo, "Apache")
    # 'sexo_abreviado' indica si es para hombres ('H') o mujeres ('M')
    
    # Determina el sexo completo (Hombre o Mujer) a partir del valor abreviado
    sexo = 'Hombre' if sexo_abreviado == 'H' else 'Mujer'
    sufijo = 'H' if sexo_abreviado == 'H' else 'M'
    
    # Crea una lista de zapatos con nombres y rutas de imágenes
    zapatos = [
        {"nombre": f"{nombre_modelo} {sexo}", "imagen": f"images/{nombre_modelo}{sufijo}{i}.png"}
        for i in range(1, 6)  # Crea 5 modelos para cada categoría
    ]
    
    # Asigna letras a cada modelo (A, B, C, ...)
    letras = list(ascii_uppercase[:len(zapatos)])
    
    # Renderiza la plantilla correspondiente a esta categoría de zapatos
    return render(request, f"categories/{nombre_modelo.lower()}_{sexo.lower()}.html", {
        "zapatos_con_letras": zip(zapatos, letras),  # Empareja cada zapato con una letra
        "colores": COLORES,  # Colores disponibles
        "tallas": TALLAS,    # Tallas disponibles
        "sexo": sexo         # Sexo de la categoría (Hombre o Mujer)
    })

# Vistas específicas que usan la vista genérica
# Estas vistas son para categorías específicas de zapatos
def apache_hombre_view(request): return categoria_view(request, "Apache", "H")
def apolo_hombre_view(request): return categoria_view(request, "Apolo", "H")
def amaka_hombre_view(request): return categoria_view(request, "Amaka", "H")
def nautico_hombre_view(request): return categoria_view(request, "Nautico", "H")
def bota_hombre_view(request): return categoria_view(request, "Bota", "H")
def casual_hombre_view(request): return categoria_view(request, "Casual", "H")
def apache_mujer_view(request): return categoria_view(request, "Apache", "M")
def bota_mujer_view(request): return categoria_view(request, "Bota", "M")

# -----------------------------
# Vista para ver los pedidos
# -----------------------------
def ver_pedidos(request):
    # Muestra los productos agregados al carrito de compras
    pedido = request.session.get('pedido', {})  # Obtiene el pedido actual desde la sesión
    return render(request, 'ver_pedidos.html', {'pedido': pedido})

# -----------------------------
# Agregar producto al pedido
# -----------------------------
def agregar_pedido(request):
    if request.method == 'POST':
        # Recibe los datos del producto a agregar
        modelo = request.POST.get('modelo')
        color = request.POST.get('color')
        talla = request.POST.get('talla')
        sexo = request.POST.get('sexo')
        imagen = request.POST.get('imagen')
        letra = request.POST.get("letra", "").upper()  # Obtiene la letra asociada con el modelo

        # Genera un código único para el zapato
        letra_sexo = sexo[0].upper()
        clave_base = f"{modelo[:2].upper()}{talla}{color[0].upper()}{letra_sexo}{letra}"

        # Obtiene el pedido actual desde la sesión
        pedido = request.session.get('pedido', {})
        contador = 1

        # Busca si ya existe un zapato con la misma clave base (modelo, color, talla, sexo)
        ids_existentes = [pid for pid in pedido.keys() if pid.startswith(clave_base)]
        if ids_existentes:
            # Si ya existe, se obtiene el número más alto para continuar con el siguiente ID
            numeros = [int(pid[len(clave_base):]) for pid in ids_existentes]
            contador = max(numeros) + 1

        # Genera el ID final del zapato
        idZapato = f"{clave_base}{str(contador).zfill(3)}"

        # Si el producto ya está en el pedido, solo se aumenta la cantidad
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
            # Si el producto no está en el pedido, se agrega con cantidad 1
            pedido[idZapato] = {
                'modelo': modelo,
                'color': color,
                'talla': talla,
                'sexo': letra_sexo,
                'cantidad': 1,
                'imagen': imagen,
                'letra': letra
            }

        # Guarda el pedido actualizado en la sesión
        request.session['pedido'] = pedido
        return redirect('ver_pedido')

# -----------------------------
# Generar archivo JSON del pedido
# -----------------------------
@login_required
def generar_pedido(request):
    if request.method == 'POST':
        # Obtiene el pedido actual desde la sesión
        pedido_data = request.session.get('pedido', {})
        
        # Si no hay productos en el carrito, muestra un error
        if not pedido_data:
            messages.error(request, "No hay productos en el carrito.")
            return redirect('ver_pedido')

        # Obtiene el comentario y cliente desde el formulario
        comentario = request.POST.get('comentario', '')
        cliente = request.POST.get('cliente', '')

        # Guarda el comentario en la sesión
        request.session['comentario'] = comentario

        # Estructura los datos del pedido
        orden_data = {
            'empleado': request.user.username,
            'cliente': cliente,
            'fecha_creacion': timezone.now().isoformat(),
            'estado': 'PENDIENTE',
            'observaciones': comentario,
            'detalles': []
        }

        # Agrega los detalles del pedido (zapatos) a la orden
        for producto in pedido_data.values():
            cantidad = int(producto.get('cantidad', 1))
            for _ in range(cantidad):
                detalle = {
                    'modelo': producto['modelo'],
                    'talla': producto['talla'],
                    'sexo': producto['sexo'],
                    'color': producto['color'],
                    'imagen': producto.get('imagen', '')
                }
                orden_data['detalles'].append(detalle)

        # Guarda el pedido como un archivo JSON
        archivos_pedidos_dir = os.path.join(settings.MEDIA_ROOT, 'archivos_pedidos')
        os.makedirs(archivos_pedidos_dir, exist_ok=True)

        # Genera un contador único para cada archivo de pedido
        contador_path = os.path.join(archivos_pedidos_dir, 'contador.json')
        if os.path.exists(contador_path):
            with open(contador_path, 'r') as f:
                contador = json.load(f).get('ultimo', 0) + 1
        else:
            contador = 1

        # Actualiza el contador para futuros pedidos
        with open(contador_path, 'w') as f:
            json.dump({'ultimo': contador}, f)

        # Añade el ID del pedido a los datos
        orden_data['id_pedido'] = contador

        # Guarda los datos del pedido en un archivo JSON
        file_name = f"pedido_{contador}.json"
        file_path = os.path.join(archivos_pedidos_dir, file_name)
        with open(file_path, 'w') as archivo:
            json.dump(orden_data, archivo, indent=4)

        # Borra el pedido de la sesión después de guardarlo
        del request.session['pedido']
        messages.success(request, f"Pedido #{contador} generado exitosamente.")
        return redirect('ver_pedido')

    # Redirige si no es una solicitud POST
    return redirect('ver_pedido')


# -----------------------------
# Eliminar producto individual del pedido
# -----------------------------
def eliminar_pedido(request):
    if request.method == 'POST':
        producto_id = request.POST.get('producto_id')
        pedido = request.session.get('pedido', {})
        if producto_id in pedido:
            del pedido[producto_id]
            request.session['pedido'] = pedido
            messages.success(request, 'Producto eliminado del carrito.')
        return redirect('ver_pedido')
    return redirect('landing')

# -----------------------------
# Eliminar todo el pedido
# -----------------------------
def eliminar_todo_pedido(request):
    if request.method == 'POST':
        if 'pedido' in request.session:
            del request.session['pedido']
            messages.success(request, 'Pedido eliminado con éxito.')
        else:
            messages.warning(request, 'No hay pedido que eliminar.')
        return redirect('ver_pedido')
    return redirect('landing')

# -----------------------------
# Actualizar cantidad de un producto
# -----------------------------
def actualizar_pedido(request):
    if request.method == 'POST':
        producto_id = request.POST.get('producto_id')
        nueva_cantidad = request.POST.get('cantidad')
        pedido = request.session.get('pedido', {})
        if producto_id in pedido and nueva_cantidad:
            try:
                nueva_cantidad = int(nueva_cantidad)
                if nueva_cantidad >= 1:
                    pedido[producto_id]['cantidad'] = nueva_cantidad
            except ValueError:
                pass
        request.session['pedido'] = pedido
    return redirect('ver_pedido')
