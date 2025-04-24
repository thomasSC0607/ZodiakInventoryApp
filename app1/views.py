from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


def csrf_failure(request, reason=""):
    return render(request, 'csrf_error.html', {'reason': reason})

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            
            login(request, user)
            return redirect('landing')  
        else:
            
            return render(request, 'login.html', {'error': 'Credenciales inválidas'})
    
    return render(request, 'login.html') 

@login_required
def landing_view(request):
    
    return render(request, 'landing.html')
def landing_view(request):
    return render(request, 'landing.html')


###
def categorias_view(request):
    return render(request, 'categorias.html')
###
def logout_view(request):
    logout(request)  
    return redirect('login')  
##
def categorias_view(request):
    categorias = [
        {"nombre": "Apache Hombre", "imagen": "images/ApacheH.png", "url": "apache_hombre"},
        {"nombre": "Apolo Hombre", "imagen": "images/ApoloH.png", "url": "apolo_hombre"},
        {"nombre": "Amaka Hombre", "imagen": "images/AmakaH.png", "url": "amaka_hombre"},
        {"nombre": "Náutico Hombre", "imagen": "images/NauticoH.png", "url": "nautico_hombre"},
        {"nombre": "Bota Hombre", "imagen": "images/BotaH.png", "url": "bota_hombre"},
        {"nombre": "Casual Hombre", "imagen": "images/CasualH.png", "url": "casual_hombre"},
        {"nombre": "Apache Mujer", "imagen": "images/ApacheM.png", "url": "apache_mujer"},
        {"nombre": "Bota Mujer", "imagen": "images/BotaM.png", "url": "bota_mujer"},
    ]
    return render(request, "categorias.html", {"categorias": categorias})