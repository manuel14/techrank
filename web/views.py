from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Cliente, Tecnico
from django.db import IntegrityError


@login_required(login_url='/web/login/')
def index(request):
    return render(request, 'web/main.html')


@login_required(login_url='/web/login/')
def seguimiento(request):
    clientes = Cliente.objects.all()
    print(clientes)
    return render(request, 'web/seguimiento.html', {'clientes': clientes})


@login_required(login_url='/web/login/')
def datos(request):
    pass


@login_required(login_url='/web/login/')
def logout_view(request):
    logout(request)
    return redirect('/web/login/')


@login_required(login_url='/web/login/')
def dato(request):
    nombre = request.POST.get("nombre", None)
    email = request.POST.get("email", None)
    telefono = request.POST.get("telefono", None)
    nodo = request.POST.get("nodo", None)
    direccion = request.POST.get("direccion", None)
    compartido = request.POST.get("compartido", None)
    id_tec = request.user.username
    tec, created = Tecnico.objects.get_or_create(tecnico_id=id_tec, user=request.user)
    cliente = Cliente(
        nombre=nombre, email=email, direccion= direccion,
        telefono=telefono, tecnico=tec,
        nodo=nodo, compartido=compartido
        )
    cliente.save()
    return render(request, 'web/seguimiento.html', {'success': True})

