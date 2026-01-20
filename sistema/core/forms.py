# sistema/core/forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Paciente, Medico, Usuario

class LoginForm(AuthenticationForm):
    # Personalizando o form de login para usar classes CSS (opcional)
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha'}))

class PacienteCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Senha")
    nome = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Nome Completo')
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}), label='Email')
    cpf = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='CPF')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Senha')
    class Meta:
        model = Paciente
        fields = ['historico_medico']
        widgets = {
            'historico_medico': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def save(self, commit=True):
        usuario = Usuario.objects.create_user(
            username=self.cleaned_data['email'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
            nome=self.cleaned_data['nome'],
            cpf=self.cleaned_data['cpf']
        )
        paciente = super().save(commit=False)
        paciente.usuario = usuario
        if commit:
            paciente.save()
        return paciente

class MedicoCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Senha")
    nome = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Nome Completo')
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}), label='Email')
    cpf = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='CPF')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Senha')

    class Meta:
        model = Medico
        fields = ['crm', 'especialidade'] 
        
    def save(self, commit=True):
        usuario = Usuario.objects.create_user(
            username=self.cleaned_data['email'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
            nome=self.cleaned_data['nome'],
            cpf=self.cleaned_data['cpf']
        )
        
        medico = super().save(commit=False)
        medico.usuario = usuario
        
        if commit:
            medico.save()
            
        return medico