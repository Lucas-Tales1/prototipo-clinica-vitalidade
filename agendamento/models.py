from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    cpf = models.CharField(max_length=11, unique=True, blank=True, null=True)
    data_nascimento = models.DateField(blank=True, null=True)
    telefone = models.CharField(max_length=11, blank=True, null=True)
    plano_saude = models.ForeignKey('Plano', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.username

class Especialidade(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()

    def __str__(self):
        return self.nome

class Servico(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    duracao_minutos = models.PositiveIntegerField()
    preco = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.nome


class Plano(models.Model):
    nome = models.CharField(max_length=50)
    observacao = models.TextField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    updated_em = models.DateTimeField(auto_now=True)
        
    def __str__(self):
        return f"Nome: {self.nome} Ultima atualização: {self.updated_em.strftime('%d/%m/%Y %H:%M:%S')}"

class Medico(models.Model):
    foto_perfil_medico = models.ImageField(upload_to="medicos/", blank=True, null=True)
    nome = models.CharField(max_length=100)
    especialidades = models.ManyToManyField(Especialidade)
    planos_aceitos = models.ManyToManyField(Plano)

    def __str__(self):
        return self.nome
    
class Paciente(models.Model):
    foto_perfil_paciente = models.ImageField(upload_to="pacientes/", blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    endereco = models.CharField(max_length=255, blank=True, null=True)
    telefone_contato = models.CharField(max_length=11, blank=True, null=True)

    def __str__(self):
        return f"Paciente: {self.user.username}"

class Consulta(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    servico = models.ForeignKey(Especialidade, on_delete=models.CASCADE)
    plano = models.ForeignKey(Plano, on_delete=models.SET_NULL, blank=True, null=True)
    data_hora = models.DateTimeField()
    criado_em = models.DateTimeField(auto_now_add=True)
    updated_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Consulta de {self.usuario.username} com {self.medico.nome} em {self.data_hora.strftime('%d/%m/%Y %H:%M')}"