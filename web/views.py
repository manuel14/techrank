from django.shortcuts import render
from django.http import HttpResponse
from .httpBasicAuth import logged_in_or_basicauth
from django.contrib.auth import logout, authenticate, login as auth_login
from django.contrib.auth.decorators import login_required

@login_required(login_url='/web/login/')
def index(request):
	return render(request, 'web/main.html')

@login_required(login_url='/web/login/')
def seguimiento(request):
	pass

@login_required(login_url='/web/login/')
def datos(request):
	pass

@login_required(login_url='/web/login/')
def logout_view(request):
    logout(request)
    return render(request, 'web/index.html')

def login(request):
    username = request.POST.get("username", None)
    password = request.POST.get("password", None)
    user = authenticate(request, username=username, password=password)
    if user is not None:
        auth_login(request, user)
        return render(request, 'web/main.html')
    else:
        return HttpResponse(status=500)

@login_required(login_url='web/login')
def dato(request):
	nombre = request.POST.get("nombre", None)
	email = request.POST.get("email", None) 
	telefono = request.POST.get("telefono", None)
	nodo = request.POST.get("nodo", None) 
	direccion  = request.POST.get("direccion", None)
	compartido = request.POST.get("compartido", None)
