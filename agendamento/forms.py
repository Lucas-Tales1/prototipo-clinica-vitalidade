# agendamento/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

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
