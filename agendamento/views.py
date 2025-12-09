from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib import messages
from .models import *
from .forms import RegisterForm
from django.contrib.auth import authenticate, login


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
            return redirect("escolher_plano")   # <<< CORRIGIDO

        messages.error(request, "Senha incorreta.")
        return redirect("login")


class EscolherPlanoView(View):
    template_name = "agendamento/escolha_plano.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        plano = request.POST.get("plano")
        request.session["plano"] = plano
        return redirect("escolha_servicos")


class EscolhaServicosView(View):
    template_name = "agendamento/escolha_servicos.html"

    def get(self, request):
        plano = request.session.get("plano")

        if plano is None:     # <<< CORRIGIDO
            return redirect("escolher_plano")

        servicos = Servico.objects.all()
        planos = Plano.objects.all()

        return render(request, self.template_name, {
            "servicos": servicos,
            "planos": planos,   # ENVIE PARA O TEMPLATE
            "plano": plano,
            "nome": request.session.get("user_name")
        })


class EscolherMedicoView(View):
    def get(self, request, servico_id):
        plano = request.session.get("plano")

        medicos = Medico.objects.filter(
            servicos__id=servico_id,
            planos_aceitos__nome__iexact=plano
        ).distinct()

        return render(request, "escolher_medico.html", {
            "medicos": medicos
        })
