# agendamento/populate_db.py
import os
import django
from datetime import date
from random import sample, choice

# Ajuste o caminho para o settings do seu projeto
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "seuprojeto.settings")
django.setup()

from agendamento.models import User, Plano, Servico, Medico

def run():
    print("Iniciando população do banco...")

    # 1️⃣ Criar usuários de teste
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="admin123",
            cpf="11111111111",
            data_nascimento="1990-01-01",
            telefone="11999999999"
        )
        print("Superusuário 'admin' criado")

    if not User.objects.filter(username="teste").exists():
        User.objects.create_user(
            username="teste",
            email="teste@example.com",
            password="teste123",
            cpf="22222222222",
            data_nascimento="1995-05-05",
            telefone="11988888888"
        )
        print("Usuário 'teste' criado")

    # 2️⃣ Criar planos
    planos_list = ["Unimed", "Bradesco Saúde", "SulAmérica", "Amil"]
    planos_obj = []
    for nome in planos_list:
        plano, created = Plano.objects.get_or_create(nome=nome)
        planos_obj.append(plano)
        if created:
            print(f"Plano '{nome}' criado")

    # 3️⃣ Criar serviços
    servicos_data = [
        {"nome": "Nutrologia", "descricao": "Consulta completa com eletrocardiograma incluso.", "preco_particular": 500},
        {"nome": "Ortopedia", "descricao": "Tratamentos de saúde musculoesquelética.", "preco_particular": 400},
        {"nome": "Geriatria", "descricao": "Reabilitação física para idosos.", "preco_particular": 350},
        {"nome": "Bioimpedância", "descricao": "Planejamento alimentar e avaliação corporal.", "preco_particular": 200},
    ]
    servicos_obj = []
    for s in servicos_data:
        servico, created = Servico.objects.get_or_create(
            nome=s["nome"],
            defaults={
                "descricao": s["descricao"],
                "preco_particular": s["preco_particular"],
                "preco": s["preco_particular"]  # opcional, igual ao particular
            }
        )
        servicos_obj.append(servico)
        if created:
            print(f"Serviço '{s['nome']}' criado")

        # Associar 2 planos aleatórios
        for plano in sample(planos_obj, 2):
            servico.planos_aceitos.add(plano)
        servico.save()

    # 4️⃣ Criar médicos
    medicos_data = [
        {"nome": "Dr. João Silva"},
        {"nome": "Dra. Maria Souza"},
        {"nome": "Dr. Pedro Lima"},
    ]
    for m in medicos_data:
        medico, created = Medico.objects.get_or_create(nome=m["nome"])
        if created:
            print(f"Médico '{m['nome']}' criado")

        # Associar serviços aleatórios
        for servico in servicos_obj:
            if choice([True, False]):
                medico.servicos.add(servico)

        # Associar planos aceitos aleatoriamente
        for plano in planos_obj:
            if choice([True, False]):
                medico.planos_aceitos.add(plano)

        medico.save()

    print("Banco populado com sucesso!")

if __name__ == "__main__":
    run()
