from django.contrib import admin
from django.urls import path
from agendamento.views import LoginView, EscolhaServicosView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login'),
    path('escolha-servicos/', EscolhaServicosView.as_view(), name='escolha_servicos'),
]
