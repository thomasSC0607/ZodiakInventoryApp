from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from .models import DetallePedido, Orden, Zapato

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
def categoria_view(request, nombre_modelo, sexo_abreviado):
    # Determina el texto completo del sexo (Hombre o Mujer)
    sexo = 'Hombre' if sexo_abreviado == 'H' else 'Mujer'
    
    # Sufijo usado para construir el nombre de la imagen (ej. "ApacheH1.png")
    sufijo = 'H' if sexo_abreviado == 'H' else 'M'

    # Crea la lista de 5 zapatos con nombre e imagen
    zapatos = [
        {"nombre": f"{nombre_modelo} {sexo}", "imagen": f"images/{nombre_modelo}{sufijo}{i}.png"}
        for i in range(1, 6)
    ]

    # Renderiza la plantilla correspondiente, pasando zapatos, colores, tallas y sexo al contexto
    return render(request, f"categories/{nombre_modelo.lower()}_{sexo.lower()}.html", {
        "zapatos": zapatos,
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
    pedido = request.session.get('pedido', {})
    return render(request, 'ver_pedidos.html', {'pedido': pedido})




def agregar_pedido(request):
    if request.method == 'POST':
        modelo = request.POST.get('modelo')
        color = request.POST.get('color')
        talla = request.POST.get('talla')
        sexo = request.POST.get('sexo')
        imagen = request.POST.get('imagen')

        letra_sexo = sexo[0].upper()
        clave_base = f"{modelo[:2].upper()}{color[0].upper()}{talla}{letra_sexo}"

        pedido = request.session.get('pedido', {})
        contador = 1

        # Buscar si ya existe una combinación parecida y encontrar el siguiente número
        ids_existentes = [pid for pid in pedido.keys() if pid.startswith(clave_base)]
        if ids_existentes:
            numeros = [int(pid[len(clave_base):]) for pid in ids_existentes]
            contador = max(numeros) + 1

        idZapato = f"{clave_base}{str(contador).zfill(3)}"

        # Revisar si ya existe un zapato igual (modelo + color + talla + sexo)
        for pid, item in pedido.items():
            if (
                item['modelo'] == modelo and
                item['color'] == color and
                str(item['talla']) == talla and
                item['sexo'] == letra_sexo
            ):
                pedido[pid]['cantidad'] += 1
                break
        else:
            # Si no existe, se agrega como nuevo
            pedido[idZapato] = {
                'modelo': modelo,
                'color': color,
                'talla': talla,
                'sexo': letra_sexo,
                'cantidad': 1,
                'imagen': imagen
            }

        request.session['pedido'] = pedido
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