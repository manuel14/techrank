from django.db import models
from django.contrib.auth.models import User

class Tecnico(models.Model):
    tecnico_id = models.IntegerField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Cliente(models.Model):

    nombre = models.CharField(max_length=150)
    direccion = models.CharField(max_length=150)
    nodo = models.CharField(max_length=150, blank=True, null=True)
    telefono = models.CharField(max_length=150)
    email = models.EmailField(max_length=150, blank=True, null=True)
    tecnico = models.ForeignKey(Tecnico, related_name="clientes")
    compartido = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'cliente'
        verbose_name_plural = 'clientes'



