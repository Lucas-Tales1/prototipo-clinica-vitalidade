from django.core.management.base import BaseCommand
from django.utils import timezone
from agendamento.models import User, Especialidade, Plano, Medico, Servico, Consulta
import random

class Command(BaseCommand):
    help = "Popula o banco com dados de demo: usuários, especialidades, planos, serviços, médicos e consultas"

    def handle(self, *args, **options):
        # Especialidades
        esp_names = [
            ("Ortopedia", "Tratamento de ossos, músculos e articulações."),
            ("Geriatria", "Cuidado da saúde do idoso."),
            ("Nutrologia", "Estudo e tratamento de distúrbios nutricionais."),
            ("Bioimpedância", "Avaliação de composição corporal."),
        ]
        especialidades = []
        for nome, desc in esp_names:
            esp, _ = Especialidade.objects.get_or_create(nome=nome, defaults={"descricao": desc})
            especialidades.append(esp)
        self.stdout.write(self.style.SUCCESS(f"Especialidades: {len(especialidades)}"))

        # Planos
        plano_nomes = ["Unimed", "Bradesco", "SulAmerica", "Amil"]
        planos = []
        for nome in plano_nomes:
            plano, _ = Plano.objects.get_or_create(nome=nome)
            planos.append(plano)
        self.stdout.write(self.style.SUCCESS(f"Planos: {len(planos)}"))

        # Serviços
        servicos_seed = [
            ("Consulta Ortopedia", "Avaliação ortopédica completa", 40, 250.00),
            ("Consulta Geriatria", "Consulta clínica para idosos", 40, 220.00),
            ("Consulta Nutrologia", "Avaliação nutricional clínica", 45, 260.00),
            ("Bioimpedância", "Exame de composição corporal", 20, 120.00),
        ]
        servicos = []
        for n, d, dur, preco in servicos_seed:
            s, _ = Servico.objects.get_or_create(nome=n, defaults={"descricao": d, "duracao_minutos": dur, "preco": preco})
            servicos.append(s)
        self.stdout.write(self.style.SUCCESS(f"Serviços: {len(servicos)}"))

        # Usuários
        users = []
        for i in range(1, 6):
            email = f"user{i}@demo.local"
            username = f"user{i}"
            user, created = User.objects.get_or_create(username=username, defaults={
                "email": email,
                "first_name": f"User{i}",
            })
            if created:
                user.set_password("demo1234")
                user.save()
            users.append(user)
        self.stdout.write(self.style.SUCCESS(f"Usuários: {len(users)}"))

        # Médicos
        nomes_medicos = [
            "Dr. Elson Augusto", "Dr. Afonso", "Dra. Carol", "Dr. Guilherme", "Dr. Marcelo Pereira",
            "Dra. Helena Costa", "Dra. Bianca Torres", "Dr. Rafael Lima", "Dr. Pedro Albuquerque", "Dr. João Figueiredo",
            "Dra. Marina Souza", "Dra. Paula Mendes",
        ]
        medicos = []
        for nome in nomes_medicos:
            m, _ = Medico.objects.get_or_create(nome=nome)
            # Atribui 1-2 especialidades aleatórias
            esp_sample = random.sample(especialidades, k=random.randint(1, 2))
            m.especialidades.set(esp_sample)
            # Atribui 2-3 planos aleatórios
            planos_sample = random.sample(planos, k=random.randint(2, 3))
            m.planos_aceitos.set(planos_sample)
            m.save()
            medicos.append(m)
        self.stdout.write(self.style.SUCCESS(f"Médicos: {len(medicos)}"))

        # Consultas futuras (por usuário)
        for user in users:
            for _ in range(random.randint(1, 3)):
                medico = random.choice(medicos)
                # Serviço compatível com especialidade primária do médico
                esp = medico.especialidades.first()
                serv_map = {
                    "Ortopedia": "Consulta Ortopedia",
                    "Geriatria": "Consulta Geriatria",
                    "Nutrologia": "Consulta Nutrologia",
                    "Bioimpedância": "Bioimpedância",
                }
                serv_name = serv_map.get(esp.nome, "Consulta Geriatria")
                servico = Servico.objects.get(nome=serv_name)
                dt = timezone.now() + timezone.timedelta(days=random.randint(1, 20), hours=random.randint(8, 18))
                Consulta.objects.get_or_create(
                    usuario=user,
                    medico=medico,
                    servico=servico,
                    data_hora=dt,
                )
        self.stdout.write(self.style.SUCCESS("Consultas futuras geradas"))

        self.stdout.write(self.style.SUCCESS("Seed de demo concluído."))
