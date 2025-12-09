from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    EscolherPlanoView,
    EscolhaServicosView,
    EscolherMedicoView,
)

urlpatterns = [
    # Autenticação
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),

    # Fluxo de agendamento
    path("escolher-plano/", EscolherPlanoView.as_view(), name="escolher_plano"),
    path("escolha-servicos/", EscolhaServicosView.as_view(), name="escolha_servicos"),
    path("escolher-medico/<int:servico_id>/", EscolherMedicoView.as_view(), name="escolher_medico"),
]
