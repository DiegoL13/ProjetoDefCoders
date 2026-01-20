# sistema/core/forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import *

class LoginForm(AuthenticationForm):
    # Personalizando o form de login para usar classes CSS (opcional)
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha'}))

class PacienteCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Senha")
    
    class Meta:
        model = Paciente
        # Liste os campos que o paciente deve preencher
        fields = ['nome', 'email', 'password', 'cpf', 'data_nascimento', 'sexo', 'contato']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            # ... adicione classes aos outros campos conforme necessário
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"]) # Criptografa a senha
        if commit:
            user.save()
        return user

class MedicoCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Senha")

    class Meta:
        model = Medico
        fields = ['nome','cpf', 'email', 'password', 'crm', 'especialidade', 'contato']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
    
