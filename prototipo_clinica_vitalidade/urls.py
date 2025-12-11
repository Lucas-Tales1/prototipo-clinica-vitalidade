from django.contrib import admin
from django.urls import path
from agendamento.views import LoginView, EscolhaServicosView, DashboardView, RegisterView
from django.conf import settings
from django.conf.urls.static import static
from agendamento.views import CriarConsultaView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('escolha-servicos/', EscolhaServicosView.as_view(), name='escolha_servicos'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('consultas/criar/', CriarConsultaView.as_view(), name='criar_consulta'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
