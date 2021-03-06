from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Tecnico(models.Model):
    tecnico_id = models.CharField(max_length=10)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.tecnico_id + " " + self.nombre

    class Meta:
        verbose_name = 'tecnico'
        verbose_name_plural = 'tecnicos'
        ordering = ('tecnico_id',)


class Cliente(models.Model):
    nombre = models.CharField(max_length=150)
    clientenro = models.CharField(max_length=100, blank=True, null=True)
    direccion = models.CharField(max_length=150)
    nodo = models.CharField(max_length=150, blank=True, null=True)
    telefono = models.CharField(max_length=150)
    email = models.EmailField(max_length=150, blank=True, null=True)
    tecnico = models.ForeignKey(
        Tecnico, related_name="clientes", on_delete=models.CASCADE)
    tecnico_compartido = models.ForeignKey(
        Tecnico, blank=True, null=True,
        default=None, related_name="clientes_comp", on_delete=models.SET_NULL)
    observacion = models.CharField(max_length=300, blank=True, null=True)
    fecha_ing = models.DateTimeField(default=timezone.now)
    fecha_liq = models.DateTimeField(
        auto_now=False, auto_now_add=False, blank=True, null=True)
    NO = "NO"
    CONTACTADO = "CT"
    VENTA = "VE"
    IN = "IN"
    LI = "LI"
    estado_choices = (
        (NO, 'No contactado'),
        (CONTACTADO, 'contactado'),
        (VENTA, 'venta confirmada'),
        (IN, "instalado"),
        (LI, 'liquidado')
    )
    estado = models.CharField(
        max_length=20, choices=estado_choices, default=NO)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'cliente'
        verbose_name_plural = 'clientes'
        unique_together = ("nombre", "direccion")
