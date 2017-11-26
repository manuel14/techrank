from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseServerError
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Cliente, Tecnico
import json

@login_required(login_url='/web/login/')
def index(request):
    return render(request, 'web/main.html')


@login_required(login_url='/web/login/')
def seguimiento(request):
    clientes = Cliente.objects.all()
    for c in clientes:
        if c.compartido:
            tec = Tecnico.objects.get(tecnico_id=c.compartido)
            c.tec_compartido = tec.nombre
    user_groups = json.dumps(list(request.user.groups.values_list('name', flat=True)))
    grupo = user_groups
    return render(request, 'web/seguimiento.html',
                  {'clientes': clientes, 'grupo': grupo})


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
    tec, created = Tecnico.objects.get_or_create(
        tecnico_id=id_tec, user=request.user)
    cliente = Cliente(
        nombre=nombre, email=email, direccion=direccion,
        telefono=telefono, tecnico=tec,
        nodo=nodo, compartido=compartido
    )
    cliente.save()
    return redirect('/web/seguimiento')


@login_required(login_url='/web/login/')
def estados(request):
    clientes_list = []
    clientes_estados = list(request.POST.dict().items())
    clientes_estados = clientes_estados[1:]
    for v in clientes_estados:
        if v[1].split("-")[1] == "no":
            pass
        else:
            clientes_dic = {
                "cliente": int(v[1].split("-")[0]), "estado": v[1].split("-")[1].upper()
            }
            clientes_list.append(clientes_dic)
    for c in clientes_list:        
        cli_obj = Cliente.objects.get(pk=c["cliente"])
        cli_obj.estado = c["estado"]
        cli_obj.save()
        if c["estado"] == "IN":
            tec_obj = Tecnico.objects.get(tecnico_id = cli_obj.tecnico.tecnico_id)
            tec_obj.cant_ventas += 1
            tec_obj.save()
            if cli_obj.compartido:
                tec_compartido = Tecnico.objects.get(tecnico_id = cli_obj.compartido)
                tec_compartido.cant_ventas += 1
                tec_compartido.save()

    return redirect('/web/seguimiento')


@login_required(login_url='/web/login/')
def ranking(request):
    tecs = Tecnico.objects.filter(
        cant_ventas__gt=0, clientes__estado="IN").order_by('-cant_ventas').distinct()
    for t in tecs:
        clientes = t.clientes.filter(estado="IN")
        t.comision = 0
        t.ventas = 0
        for c in clientes:
            t.ventas +=1
            if c.compartido is None or c.compartido == "":
                t.comision += 150   
            else:
                t.comision += 75

    return render(request, 'web/ranking.html', {'tecnicos': tecs})

def error404(request):
    return render(request, 'web/404.html')

def error500(request):
    return render(request, 'web/500.html')