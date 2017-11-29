from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseServerError
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Cliente, Tecnico
from django.db.models import Count, Q
from django.contrib.auth.models import User
import json
import pytz

@login_required(login_url='/web/login/')
def index(request):
    return render(request, 'web/main.html')


@login_required(login_url='/web/login/')
def seguimiento(request):
    clientes = Cliente.objects.all()
    for c in clientes:
        tz = pytz.timezone('America/Argentina/Buenos_Aires')
        c.fecha = c.fecha_ing.astimezone(tz)
    user_groups = json.dumps(list(request.user.groups.values_list('name', flat=True)))
    return render(request, 'web/seguimiento.html',
                  {'clientes': clientes, 'grupo': user_groups})


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
    if compartido:
        user = User.objects.get(username=compartido)
        tec_comp, created = Tecnico.objects.get_or_create(
            tecnico_id=compartido, user=user)
    else:
        tec_comp = None
    cliente = Cliente(
        nombre=nombre, email=email, direccion=direccion,
        telefono=telefono, tecnico=tec,
        nodo=nodo, tecnico_compartido=tec_comp
    )
    cliente.save()
    return redirect('/web/seguimiento')


@login_required(login_url='/web/login/')
def estados(request):
    clientes_list = []
    clientes_estados = list(request.POST.dict().items())
    print(clientes_estados)
    clientes_estados = [(x,y) for (x,y) in clientes_estados if x != "csrfmiddlewaretoken" ]
    for v in clientes_estados:
        try:
            if v[1].split("-")[1] == "no":
                pass
            else:
                clientes_dic = {
                    "cliente": int(v[1].split("-")[0]), 
                    "estado": v[1].split("-")[1].upper(),
                    "obs": None
                }
                clientes_list.append(clientes_dic)
        except IndexError:
            clientes_dic = {
                "cliente": v[0].split("-")[1], 
                "obs": v[1].strip(), "estado": None
            }
            clientes_list.append(clientes_dic)
    for c in clientes_list:        
        cli_obj = Cliente.objects.get(pk=c["cliente"])
        if c["estado"]:
            cli_obj.estado = c["estado"]
        if c["obs"]:
            cli_obj.observacion = c["obs"]
        cli_obj.save()

    return redirect('/web/seguimiento')


@login_required(login_url='/web/login/')
def ranking(request):
    tecs = Tecnico.objects.filter(
        Q(clientes__estado__in=["IN", "LI"])|Q(clientes_comp__estado__in=["LI", "IN"])).distinct()
    for t in tecs:
        clientes = t.clientes.filter(estado__in=["LI", "IN"])
        clientes_comp = t.clientes_comp.filter(estado__in=["LI", "IN"])
        t.comision = 0
        t.ventas = 0
        for c in clientes:
            t.ventas +=1
            if c.tecnico_compartido is None:
                t.comision += 150   
            else:
                t.comision += 75
        for c in clientes_comp:
            t.ventas +=1
            if c.tecnico_compartido is None:
                t.comision += 150   
            else:
                t.comision += 75
    tecs = sorted(tecs, key=lambda t:t.ventas, reverse=True)
    return render(request, 'web/ranking.html', {'tecnicos': tecs})

def error404(request):
    return render(request, 'web/404.html')

def error500(request):
    return render(request, 'web/500.html')