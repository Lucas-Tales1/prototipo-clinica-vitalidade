from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Plano)
admin.site.register(Servico)
admin.site.register(Agendamento)
admin.site.register(Medico)