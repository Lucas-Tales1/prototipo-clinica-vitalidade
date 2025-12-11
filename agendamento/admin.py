from django.contrib import admin
from .models import User, Especialidade, Servico, Plano, Medico, Consulta, Paciente

admin.site.register(User)
admin.site.register(Especialidade)
admin.site.register(Servico)
admin.site.register(Plano)
admin.site.register(Medico)
admin.site.register(Consulta)
admin.site.register(Paciente)
