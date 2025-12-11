# agendamento/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Consulta, Medico, Servico, Plano, Especialidade

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "cpf", "data_nascimento", "telefone"]

        widgets = {
            "username": forms.TextInput(attrs={
                "class": "input",
                "placeholder": "seu_usuario"
            }),
            "email": forms.EmailInput(attrs={
                "class": "input",
                "placeholder": "exemplo@clinicavitalidade.com.br"
            }),
            "cpf": forms.TextInput(attrs={
                "class": "input",
                "placeholder": "00000000000"
            }),
            "data_nascimento": forms.DateInput(attrs={
                "type": "date",
                "class": "input"
            }),
            "telefone": forms.TextInput(attrs={
                "class": "input",
                "placeholder": "11999999999"
            }),
        }

    # sobrescrevendo widgets das senhas
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs.update({
            "class": "input",
            "placeholder": "••••••••••••"
        })
        self.fields["password2"].widget.attrs.update({
            "class": "input",
            "placeholder": "••••••••••••"
        })

class ConsultaCreateForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ["usuario", "medico", "servico", "plano", "data_hora"]
        widgets = {
            "usuario": forms.Select(attrs={"class": "input"}),
            "medico": forms.Select(attrs={"class": "input"}),
            "servico": forms.Select(attrs={"class": "input"}),
            "plano": forms.Select(attrs={"class": "input"}),
            "data_hora": forms.DateTimeInput(attrs={"type": "datetime-local", "class": "input"}),
        }

    def __init__(self, *args, **kwargs):
        # Allow passing a user to preselect and restrict plan choices
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields["usuario"].initial = user.pk
            # If user has a plan, preselect it
            if getattr(user, "plano_saude", None):
                self.fields["plano"].initial = user.plano_saude_id
        # Optional: order dropdowns for better UX
        self.fields["medico"].queryset = Medico.objects.order_by("nome")
        self.fields["servico"].queryset = Especialidade.objects.order_by("nome")
        self.fields["plano"].queryset = Plano.objects.order_by("nome")