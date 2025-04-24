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

from django.shortcuts import render

def apache_hombre_view(request):
    zapatos = [
        {"nombre": "Apache Hombre", "imagen": "images/ApacheH1.png"},
        {"nombre": "Apache Hombre", "imagen": "images/ApacheH2.png"},
        {"nombre": "Apache Hombre", "imagen": "images/ApacheH3.png"},
        {"nombre": "Apache Hombre", "imagen": "images/ApacheH4.png"},
        {"nombre": "Apache Hombre", "imagen": "images/ApacheH5.png"},
    ]
    return render(request, "categories/apache_hombre.html", {"zapatos": zapatos})


def apolo_hombre_view(request):
    zapatos = [
        {"nombre": "Apolo Hombre", "imagen": "images/ApoloH1.png"},
        {"nombre": "Apolo Hombre", "imagen": "images/ApoloH2.png"},
        {"nombre": "Apolo Hombre", "imagen": "images/ApoloH3.png"},
        {"nombre": "Apolo Hombre", "imagen": "images/ApoloH4.png"},
        {"nombre": "Apolo Hombre", "imagen": "images/ApoloH5.png"},
    ]
    return render(request, "categories/apolo_hombre.html", {"zapatos": zapatos})


def amaka_hombre_view(request):
    zapatos = [
        {"nombre": "Amaka Hombre", "imagen": "images/AmakaH1.png"},
        {"nombre": "Amaka Hombre", "imagen": "images/AmakaH2.png"},
        {"nombre": "Amaka Hombre", "imagen": "images/AmakaH3.png"},
        {"nombre": "Amaka Hombre", "imagen": "images/AmakaH4.png"},
        {"nombre": "Amaka Hombre", "imagen": "images/AmakaH5.png"},
    ]
    return render(request, "categories/amaka_hombre.html", {"zapatos": zapatos})


def nautico_hombre_view(request):
    zapatos = [
        {"nombre": "Náutico Hombre", "imagen": "images/NauticoH1.png"},
        {"nombre": "Náutico Hombre", "imagen": "images/NauticoH2.png"},
        {"nombre": "Náutico Hombre", "imagen": "images/NauticoH3.png"},
        {"nombre": "Náutico Hombre", "imagen": "images/NauticoH4.png"},
        {"nombre": "Náutico Hombre", "imagen": "images/NauticoH5.png"},
    ]
    return render(request, "categories/nautico_hombre.html", {"zapatos": zapatos})


def bota_hombre_view(request):
    zapatos = [
        {"nombre": "Bota Hombre", "imagen": "images/BotaH1.png"},
        {"nombre": "Bota Hombre", "imagen": "images/BotaH2.png"},
        {"nombre": "Bota Hombre", "imagen": "images/BotaH3.png"},
        {"nombre": "Bota Hombre", "imagen": "images/BotaH4.png"},
        {"nombre": "Bota Hombre", "imagen": "images/BotaH5.png"},
    ]
    return render(request, "categories/bota_hombre.html", {"zapatos": zapatos})


def casual_hombre_view(request):
    zapatos = [
        {"nombre": "Casual Hombre", "imagen": "images/CasualH1.png"},
        {"nombre": "Casual Hombre", "imagen": "images/CasualH2.png"},
        {"nombre": "Casual Hombre", "imagen": "images/CasualH3.png"},
        {"nombre": "Casual Hombre", "imagen": "images/CasualH4.png"},
        {"nombre": "Casual Hombre", "imagen": "images/CasualH5.png"},
    ]
    return render(request, "categories/casual_hombre.html", {"zapatos": zapatos})


def apache_mujer_view(request):
    zapatos = [
        {"nombre": "Apache Mujer", "imagen": "images/ApacheM1.png"},
        {"nombre": "Apache Mujer", "imagen": "images/ApacheM2.png"},
        {"nombre": "Apache Mujer", "imagen": "images/ApacheM3.png"},
        {"nombre": "Apache Mujer", "imagen": "images/ApacheM4.png"},
        {"nombre": "Apache Mujer", "imagen": "images/ApacheM5.png"},
    ]
    return render(request, "categories/apache_mujer.html", {"zapatos": zapatos})


def bota_mujer_view(request):
    zapatos = [
        {"nombre": "Bota Mujer", "imagen": "images/BotaM1.png"},
        {"nombre": "Bota Mujer", "imagen": "images/BotaM2.png"},
        {"nombre": "Bota Mujer", "imagen": "images/BotaM3.png"},
        {"nombre": "Bota Mujer", "imagen": "images/BotaM4.png"},
        {"nombre": "Bota Mujer", "imagen": "images/BotaM5.png"},
    ]
    return render(request, "categories/bota_mujer.html", {"zapatos": zapatos})
