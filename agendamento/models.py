from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    cpf = models.CharField(max_length=11, unique=True)
    data_nascimento = models.DateField()
    telefone = models.CharField(max_length=11)

class Plano(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome


class Servico(models.Model):
    nome = models.CharField(max_length=50)
    preco_particular = models.DecimalField(max_digits=7, decimal_places=2)
    descricao = models.TextField(blank=True, null=True)
    preco = models.DecimalField(max_digits=8, decimal_places=2, default=0,blank=True, null=True)
    planos_aceitos = models.ManyToManyField(Plano, blank=True) 
    
    def __str__(self):
        return self.nome


class Medico(models.Model): 
    nome = models.CharField(max_length=100)
    foto = models.ImageField(upload_to="medicos/", blank=True, null=True)

    servicos = models.ManyToManyField(Servico)
    planos_aceitos = models.ManyToManyField(Plano)

    def __str__(self):
        return self.nome


class Agendamento(models.Model):
    paciente = models.ForeignKey(User, on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE)
    plano = models.ForeignKey(Plano, on_delete=models.SET_NULL, null=True)
    data = models.DateField()
    hora = models.TimeField()

    def __str__(self):
        return f"{self.paciente} - {self.servico} - {self.data}"