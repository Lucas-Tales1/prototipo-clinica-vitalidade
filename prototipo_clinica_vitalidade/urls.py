from django.contrib import admin
from django.urls import path
from agendamento.views import LoginView, EscolhaServicosView, DashboardView, RegisterView, AgendaAtendenteView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('escolha-servicos/', EscolhaServicosView.as_view(), name='escolha_servicos'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('agenda-atendente/', AgendaAtendenteView.as_view(), name='agenda_atendente'),
]
