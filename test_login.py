#!/usr/bin/env python
import os
import sys
import django

sys.path.insert(0, 'C:\\Users\\Domi\\Downloads\\PortalSaude-fixed_bugs\\PortalSaude-Continuacao\\sistema')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema.settings')

django.setup()

from django.test import Client
from core.models import Paciente, Medico
import random
import string

def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def generate_valid_cpf():
    # Generate a valid CPF (simplified)
    digits = [random.randint(0, 9) for _ in range(9)]
    # Calculate first check digit
    soma = sum(digits[i] * (10 - i) for i in range(9))
    resto = soma % 11
    digito1 = 0 if resto < 2 else 11 - resto
    digits.append(digito1)
    # Calculate second check digit
    soma = sum(digits[i] * (11 - i) for i in range(10))
    resto = soma % 11
    digito2 = 0 if resto < 2 else 11 - resto
    digits.append(digito2)
    if all(d == digits[0] for d in digits):
        return '52998224725'
    return ''.join(str(d) for d in digits)

def test_paciente_login():
    print("Testing paciente login...")
    client = Client()
    
    # Create a paciente
    unique_id = generate_random_string(6)
    email = f'test.paciente.{unique_id}@example.com'
    cpf = generate_valid_cpf()
    password = 'testpassword123'
    
    paciente = Paciente.objects.create_user(
        email=email,
        password=password,
        nome=f'Paciente Teste {unique_id}',
        cpf=cpf,
        data_nascimento='1990-05-15',
        sexo='feminino',
        contato='(11) 98888-7777'
    )
    
    print(f"Created paciente: {email}")
    
    # Attempt login
    response = client.post('/login/', {'username': email, 'password': password})
    print(f"Login response status: {response.status_code}")
    print(f"Redirect URL: {response.url if response.status_code == 302 else 'No redirect'}")
    
    if response.status_code == 302:
        # Follow redirect
        response2 = client.get(response.url)
        print(f"Redirected to: {response2.status_code}")
        print(f"Final URL: {response2.request['PATH_INFO']}")
        # Check if page contains paciente dashboard elements
        if 'Meus Exames' in response2.content.decode('utf-8', errors='ignore'):
            print("[SUCCESS] Paciente login and redirect successful!")
        else:
            print("[WARNING] Patient dashboard not detected.")
    else:
        print("[ERROR] Login failed or no redirect.")
        # Print response content for debugging
        print(response.content[:500])
    
    # Clean up
    paciente.delete()
    print("Cleaned up test paciente.")

def test_medico_login():
    print("\nTesting médico login...")
    client = Client()
    
    unique_id = generate_random_string(6)
    email = f'test.medico.{unique_id}@example.com'
    cpf = generate_valid_cpf()
    password = 'testpassword123'
    
    medico = Medico.objects.create_user(
        email=email,
        password=password,
        nome=f'Dr. Teste Médico {unique_id}',
        cpf=cpf,
        crm=f'CRM-SP-{unique_id}',
        especialidade='Cardiologia',
        data_nascimento='1980-01-01',
        sexo='masculino',
        contato='(11) 99999-8888'
    )
    
    print(f"Created médico: {email}")
    
    response = client.post('/login/', {'username': email, 'password': password})
    print(f"Login response status: {response.status_code}")
    print(f"Redirect URL: {response.url if response.status_code == 302 else 'No redirect'}")
    
    if response.status_code == 302:
        response2 = client.get(response.url)
        print(f"Redirected to: {response2.status_code}")
        print(f"Final URL: {response2.request['PATH_INFO']}")
        if 'Dashboard' in response2.content.decode('utf-8', errors='ignore'):
            print("[SUCCESS] Médico login and redirect successful!")
        else:
            print("[WARNING] Médico dashboard not detected.")
    else:
        print("[ERROR] Login failed or no redirect.")
        print(response.content[:500])
    
    medico.delete()
    print("Cleaned up test médico.")

if __name__ == '__main__':
    test_paciente_login()
    test_medico_login()