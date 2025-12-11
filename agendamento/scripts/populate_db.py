import random
from datetime import datetime, timedelta
from django.utils import timezone
from agendamento.models import User, Paciente, Medico, Especialidade, Servico, Plano, Consulta

# ===============================
# Planos
# ===============================
planos = [
    {"nome": "Unimed Nacional"},
    {"nome": "Bradesco Saúde"},
    {"nome": "Amil 400"},
]

plano_objs = []
for p in planos:
    plano_obj, _ = Plano.objects.get_or_create(nome=p["nome"])
    plano_objs.append(plano_obj)

# ===============================
# Especialidades
# ===============================
especialidades = ["Nutrologia", "Geriatria", "Ortopedia", "Bioimpedância"]

especialidade_objs = []
for nome in especialidades:
    e, _ = Especialidade.objects.get_or_create(nome=nome, descricao=f"Especialidade de {nome}")
    especialidade_objs.append(e)

# ===============================
# Serviços
# ===============================
servicos = []
for nome in especialidades:
    s, _ = Servico.objects.get_or_create(
        nome=nome,
        descricao=f"Serviço de {nome}",
        duracao_minutos=60,
        preco=random.randint(100, 500)
    )
    servicos.append(s)

# ===============================
# Médicos
# ===============================
medicos_data = [
    {"nome": "Dr. Elson Augusto", "especialidades": ["Nutrologia"]},
    {"nome": "Dra. Carol", "especialidades": ["Geriatria"]},
    {"nome": "Dr. Marcos", "especialidades": ["Ortopedia"]},
    {"nome": "Dra. Fernanda", "especialidades": ["Bioimpedância", "Nutrologia"]},
]

medico_objs = []
for m in medicos_data:
    medico, _ = Medico.objects.get_or_create(nome=m["nome"])
    # Adiciona especialidades
    medico.especialidades.clear()
    for esp_nome in m["especialidades"]:
        esp_obj = Especialidade.objects.get(nome=esp_nome)
        medico.especialidades.add(esp_obj)
    # Adiciona todos os planos
    for plano in plano_objs:
        medico.planos_aceitos.add(plano)
    medico_objs.append(medico)

# ===============================
# Pacientes / Usuários
# ===============================
pacientes_data = [
    {"username": "lucas", "first_name": "Lucas", "last_name": "Tales", "email": "lucas@example.com", "cpf": "12345678901"},
    {"username": "ana", "first_name": "Ana", "last_name": "Silva", "email": "ana@example.com", "cpf": "10987654321"},
    {"username": "bruno", "first_name": "Bruno", "last_name": "Pereira", "email": "bruno@example.com", "cpf": "23456789012"},
]

paciente_objs = []
for u in pacientes_data:
    user, created = User.objects.get_or_create(
        username=u["username"],
        defaults={
            "first_name": u["first_name"],
            "last_name": u["last_name"],
            "email": u["email"],
            "cpf": u["cpf"],
        }
    )
    if created:
        user.set_password("123456")  # Senha padrão
        user.plano_saude = random.choice(plano_objs)
        user.save()

    # Cria o paciente
    paciente, _ = Paciente.objects.get_or_create(user=user)
    paciente_objs.append(paciente)

# ===============================
# Consultas
# ===============================
print("Criando consultas...")

for paciente in paciente_objs:
    for _ in range(3):  # 3 consultas por paciente
        medico = random.choice(medico_objs)
        servico = random.choice(servicos)
        plano = paciente.user.plano_saude
        data_hora = timezone.now() + timedelta(days=random.randint(1, 30), hours=random.randint(8, 17))
        Consulta.objects.create(
            usuario=paciente.user,
            medico=medico,
            servico=servico,
            plano=plano,
            data_hora=data_hora
        )

print("Banco populado com sucesso!")
