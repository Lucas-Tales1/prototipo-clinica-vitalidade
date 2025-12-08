from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView


class LoginView(View):
    template_name = "agendamento/login.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get("login", "").strip()
        name = ""
        if email:
            local_part = email.split("@")[0]
            parts = [p for p in local_part.replace("_", ".").split(".") if p]
            if parts:
                name = " ".join(s.capitalize() for s in parts)
            else:
                name = local_part.capitalize()
        # Armazena temporariamente nome e email na sessão e redireciona para escolha de serviços
        request.session["user_name"] = name
        request.session["user_email"] = email
        return redirect("escolha_servicos")


class EscolhaServicosView(View):
    template_name = "agendamento/escolha_servicos.html"

    def get(self, request):
        # Recupera dados da sessão para personalizar a página
        context = {
            "name": request.session.get("user_name", ""),
            "email": request.session.get("user_email", ""),
        }
        return render(request, self.template_name, context)


class DashboardView(TemplateView):
    template_name = "agendamento/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Inclui informações do usuário da sessão, mantendo baixo acoplamento
        context.update({
            "name": self.request.session.get("user_name", ""),
            "email": self.request.session.get("user_email", ""),
        })
        return context
