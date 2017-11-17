from django.db import models
from django.contrib.auth import User

class Cliente(models.Model):

    nombre = models.CharField(max_length=150)
    direccion = models.CharField(max_length=150)
    nodo = models.CharField(max_length=150)
    telefono = models.CharField(max_length=150)
    email = models.EmailField(max_length=150)
    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'cliente'
        verbose_name_plural = 'clientes'

class Tecnico(models.model):
	tecnico_id = models.IntegerField()
	user = models.OneToOneField(User, on_delete=models.CASCADE)
