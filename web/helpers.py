from django.db.models import Q
from .models import Tecnico


def ranking_tecs():
    tecs = Tecnico.objects.filter(
        Q(clientes__estado="LI") | Q(clientes_comp__estado="LI") & Q()).distinct()
    for t in tecs:
        clientes = t.clientes.filter(estado="LI")
        clientes_comp = t.clientes_comp.filter(estado="LI")
        t.comision = 0
        t.ventas = 0
        for c in clientes:
            t.ventas += 1
            if c.tecnico_compartido is None:
                t.comision += 150
            else:
                t.comision += 75
        for c in clientes_comp:
            t.ventas += 1
            if c.tecnico_compartido is None:
                t.comision += 150
            else:
                t.comision += 75
    tecs = sorted(tecs, key=lambda t: t.ventas, reverse=True)
    return tecs
