from django.shortcuts import render, redirect
from django.views import View
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib import messages
from .models import User, Consulta, Medico, Servico, Plano, Especialidade
from .forms import RegisterForm, ConsultaCreateForm
from django.contrib.auth import authenticate, login
from django.views.generic import TemplateView
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.http import HttpResponseBadRequest
from django.db.models import Q
import time



class RegisterView(CreateView):
    model = User
    template_name = "agendamento/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Conta criada com sucesso! Faça login para continuar.")
        return redirect("login")

    def form_invalid(self, form):
        messages.error(self.request, "Corrija os erros abaixo.")
        print(form.errors)
        return super().form_invalid(form)


class LoginView(View):
    template_name = "agendamento/login.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get("login")
        password = request.POST.get("password")

        try:
            user_obj = User.objects.get(email=email)
            username = user_obj.username
        except User.DoesNotExist:
            messages.error(request, "Email não encontrado.")
            return redirect("login")

        if not email or not password:
            messages.error(request, "Preencha email e senha.")
            return redirect("login")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")   # <<< CORRIGIDO

        messages.error(request, "Senha incorreta.")
        return redirect("login")


class EscolhaServicosView(View):
    template_name = "agendamento/escolha_servicos.html"

    def get(self, request):
        context = {
            "name": request.session.get("user_name", ""),
            "email": request.session.get("user_email", ""),
            "medicos": Medico.objects.select_related().prefetch_related("especialidades", "planos_aceitos").order_by("nome"),
            "servicos": Servico.objects.order_by("nome"),
        }
        return render(request, self.template_name, context)


class DashboardView(TemplateView):
    template_name = "agendamento/dashboard.html"

    def _get_user_context(self):
        user = self.request.user if self.request.user.is_authenticated else None
        if user:
            full_name = user.get_full_name().strip() or user.username
            first_name = (user.first_name or full_name or user.username).strip()
            email = user.email
        else:
            # Fallback em caso de usuário anônimo
            full_name = self.request.session.get("user_name", "") or ""
            first_name = full_name.split(" ")[0] if full_name else ""
            email = self.request.session.get("user_email", "") or ""
        return {
            "user_full_name": full_name,
            "user_first_name": first_name,
            "user_email": email,
        }

    def _get_consultas(self):
        if not self.request.user.is_authenticated:
            return Consulta.objects.none()
        now = timezone.now()
        return (Consulta.objects
                .select_related("medico", "servico", "usuario")
                .filter(usuario=self.request.user)
                .order_by("-data_hora"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self._get_user_context())
        context["consultas"] = self._get_consultas()
        return context


class CriarConsultaView(View):
    def post(self, request):
        # print("Dados recebidos para agendamento:", request.POST)
        if not request.user.is_authenticated:
            # messages.error(request, "Você precisa estar logado para agendar.")
            return redirect("login")

        # usuario_id = request.POST.get("usuario_id")
        medico_id = request.POST.get("medico_id")
        servico_id = request.POST.get("especialidade_id")
        data_hora_str = request.POST.get("data_hora")

        if not (medico_id and servico_id and data_hora_str):
            return HttpResponseBadRequest("Dados insuficientes para agendamento.")

        # # Plano do paciente (pode ser None)
        plano_id = getattr(request.user, "plano_saude_id", None)

        print(f"Agendamento - Usuário: {request.user.id}, Médico: {medico_id}, Serviço: {servico_id},Plano: {plano_id}, Data/Hora: {data_hora_str}")

        # # Monta payload para o ModelForm
        form_data = {
            "usuario": request.user.id,
            "medico": medico_id,
            "servico": servico_id,
            "plano": plano_id,
            "data_hora": data_hora_str,  # formato esperado: YYYY-MM-DDTHH:MM
        }

        form = ConsultaCreateForm(data=form_data, user=request.user)
        print("Form data para agendamento:", form)

        # # Valida médico e serviço existem e plano é aceito
        try:
            medico = Medico.objects.get(id=medico_id)
            servico = Especialidade.objects.get(id=servico_id)
        except (Medico.DoesNotExist, Especialidade.DoesNotExist):
            return HttpResponseBadRequest("Médico ou serviço inválido.")

        if plano_id:
            if not medico.planos_aceitos.filter(id=plano_id).exists():
                # messages.error(request, "Este médico não aceita o seu plano de saúde.")
                return redirect("escolha_servicos")

        if form.is_valid():
            consulta = form.save()
            # messages.success(request, "Consulta criada com sucesso!")
            # time.sleep(1) 
            return redirect("dashboard")

        # # Erros de form
        # messages.error(request, "Corrija os dados do agendamento.")
        return redirect("escolha_servicos")

    def get(self, request):
        return HttpResponseBadRequest("Método não permitido.")
