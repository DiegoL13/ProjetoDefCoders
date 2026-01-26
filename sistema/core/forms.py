# sistema/core/forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import *

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'E-mail'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha'}))

class PacienteCreationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}), 
        label="Senha",
        min_length=6
    )
    cpf = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'XXX.XXX.XXX-XX'}), 
        label="CPF",
        max_length=14  # Permitir CPF formatado XXX.XXX.XXX-XX
    )
    
    class Meta:
        model = Paciente
        fields = ['nome', 'email', 'password', 'cpf', 'data_nascimento', 'sexo', 'contato', 'historico_medico']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Seu nome completo'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'seu@email.com'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'XXX.XXX.XXX-XX'}),
            'data_nascimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'sexo': forms.Select(attrs={'class': 'form-control'}),
            'contato': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(DD) XXXXX-XXXX'}),
            'historico_medico': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Descreva seu histórico médico...'}),
        }

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if cpf:
            cpf = ''.join(filter(str.isdigit, cpf))  # Remove caracteres não numéricos
            if len(cpf) != 11:
                raise forms.ValidationError('CPF deve ter 11 dígitos.')
            
            # Validação completa do CPF
            # Verificar se todos os dígitos são iguais
            if cpf == cpf[0] * len(cpf):
                raise forms.ValidationError('CPF inválido.')
            
            # Cálculo dos dígitos verificadores
            soma = 0
            for i in range(9):
                soma += int(cpf[i]) * (10 - i)
            
            resto = soma % 11
            digito1 = 0 if resto < 2 else 11 - resto
            
            soma = 0
            for i in range(10):
                soma += int(cpf[i]) * (11 - i)
            
            resto = soma % 11
            digito2 = 0 if resto < 2 else 11 - resto
            
            # Verificar os dígitos verificadores
            if int(cpf[9]) != digito1 or int(cpf[10]) != digito2:
                raise forms.ValidationError('CPF inválido.')
        
        return cpf

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError('Este e-mail já está cadastrado.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class MedicoCreationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}), 
        label="Senha",
        min_length=6
    )
    cpf = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'XXX.XXX.XXX-XX'}), 
        label="CPF",
        max_length=14  # Permitir CPF formatado XXX.XXX.XXX-XX
    )
    
    class Meta:
        model = Medico
        fields = ['nome','cpf', 'email', 'password', 'crm', 'especialidade', 'contato', 'data_nascimento', 'sexo']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Seu nome completo'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'seu@email.com'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'XXX.XXX.XXX-XX'}),
            'data_nascimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'sexo': forms.Select(attrs={'class': 'form-control'}),
            'contato': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(DD) XXXXX-XXXX'}),
            'crm': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CRM-UF XXXXX'}),
            'especialidade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Cardiologia'}),
        }

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if cpf:
            cpf = ''.join(filter(str.isdigit, cpf))  # Remove caracteres não numéricos
            if len(cpf) != 11:
                raise forms.ValidationError('CPF deve ter 11 dígitos.')
            
            # Validação completa do CPF
            # Verificar se todos os dígitos são iguais
            if cpf == cpf[0] * len(cpf):
                raise forms.ValidationError('CPF inválido.')
            
            # Cálculo dos dígitos verificadores
            soma = 0
            for i in range(9):
                soma += int(cpf[i]) * (10 - i)
            
            resto = soma % 11
            digito1 = 0 if resto < 2 else 11 - resto
            
            soma = 0
            for i in range(10):
                soma += int(cpf[i]) * (11 - i)
            
            resto = soma % 11
            digito2 = 0 if resto < 2 else 11 - resto
            
            # Verificar os dígitos verificadores
            if int(cpf[9]) != digito1 or int(cpf[10]) != digito2:
                raise forms.ValidationError('CPF inválido.')
        
        return cpf

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError('Este e-mail já está cadastrado.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
    
