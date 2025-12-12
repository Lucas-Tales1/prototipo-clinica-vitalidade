# agendamento/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Consulta, Medico, Servico, Plano



class RegisterForm(UserCreationForm):
    # Declarado explicitamente para controlar widget/empty_label/ordenacao
    plano_saude = forms.ModelChoiceField(
        queryset=Plano.objects.all(),
        required=False,
        label="Plano de Saúde",
        widget=forms.Select(attrs={"class": "input"}),
        empty_label="Selecione um plano"
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "cpf",
            "data_nascimento",
            "telefone",
            "plano_saude",  # garante que o ModelForm trate esse campo
        ]
        widgets = {
            "username": forms.TextInput(attrs={"class": "input", "placeholder": "digite seu nome"}),
            "email": forms.EmailInput(attrs={"class": "input", "placeholder": "exemplo@clinicavitalidade.com.br"}),
            "cpf": forms.TextInput(attrs={"class": "input", "placeholder": "00000000000"}),
            "data_nascimento": forms.DateInput(attrs={"type": "date","class": "input","placeholder": "dd/mm/aaaa"}),
            "telefone": forms.TextInput(attrs={"class": "input", "placeholder": "11999999999"}),
            # não estritamente necessário repetir plano_saude aqui, já declaramos acima,
            # mas não faz mal manter para consistência:
            "plano_saude": forms.Select(attrs={"class": "input"}),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # garante as classes nos campos de senha
        if "password1" in self.fields:
            self.fields["password1"].widget.attrs.update({
                "class": "input",
                "placeholder": "••••••••••••"
            })
        if "password2" in self.fields:
            self.fields["password2"].widget.attrs.update({
                "class": "input",
                "placeholder": "••••••••••••"
            })

        # Se quiser alterar o label do campo (apenas visual)
        self.fields["plano_saude"].label = "Plano de Saúde"
        
        # Mostrar apenas o nome do plano no select (não altera __str__ do modelo)
        self.fields["plano_saude"].label_from_instance = lambda obj: obj.nome

        self.fields["cpf"].label = "CPF"
        self.fields["cpf"].help_text = "Apenas números, sem pontos ou traços."
        
        self.fields["username"].label = "Nome"
        self.fields["email"].label = "Email"
        self.fields["password1"].label = "Senha"
        self.fields["password2"].label = "Confirmar Senha"

    def clean_username(self):
        username = self.cleaned_data.get("username", "")
        username = username.strip().replace(" ", "_")
        # opcional: forçar lower() e remover chars indesejados
        # username = re.sub(r'[^a-zA-Z0-9_.-]', '', username).lower()
        return username

    def save(self, commit=True):
        # Garantir que o plano seja atribuído corretamente ao model User
        user = super().save(commit=False)
        user.plano_saude = self.cleaned_data.get("plano_saude")  # pode ser None
        if commit:
            user.save()
        return user


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
        self.fields["servico"].queryset = Servico.objects.order_by("nome")
        self.fields["plano"].queryset = Plano.objects.order_by("nome")
