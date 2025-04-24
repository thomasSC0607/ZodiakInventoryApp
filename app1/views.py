from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

def csrf_failure(request, reason=""):
    return render(request, 'csrf_error.html', {'reason': reason})

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        # Autenticación del usuario
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Iniciar sesión y redirigir a landing
            login(request, user)
            return redirect('landing')  # Redirección a la página de landing
        else:
            # Si las credenciales no son correctas, enviar error
            return render(request, 'login.html', {'error': 'Credenciales inválidas'})
    
    return render(request, 'login.html')  # Mostrar la página de login si no es POST

@login_required
def landing_view(request):
    # Vista de la página principal después de login
    return render(request, 'landing.html')
