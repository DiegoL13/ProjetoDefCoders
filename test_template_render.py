#!/usr/bin/env python
import os
import sys
import django

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'sistema'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema.settings')

django.setup()

from django.test import Client
from core.models import Paciente
import random
import string

def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def generate_valid_cpf():
    digits = [random.randint(0, 9) for _ in range(9)]
    soma = sum(digits[i] * (10 - i) for i in range(9))
    resto = soma % 11
    digito1 = 0 if resto < 2 else 11 - resto
    digits.append(digito1)
    soma = sum(digits[i] * (11 - i) for i in range(10))
    resto = soma % 11
    digito2 = 0 if resto < 2 else 11 - resto
    digits.append(digito2)
    if all(d == digits[0] for d in digits):
        return '52998224725'
    return ''.join(str(d) for d in digits)

def test_template_with_paciente():
    print("Testing template rendering with paciente user...")
    client = Client()
    
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
    
    # Login
    client.login(username=email, password=password)
    
    # Debug: get user and check properties
    from django.contrib.auth import get_user_model
    User = get_user_model()
    user = User.objects.get(email=email)
    print(f"User ID: {user.id}")
    print(f"User is_paciente: {user.is_paciente}")
    print(f"User is_medico: {user.is_medico}")
    print(f"Hasattr paciente: {hasattr(user, 'paciente')}")
    if hasattr(user, 'paciente'):
        print(f"Paciente ID: {user.paciente.id}")
    
    # Access paciente exames page (includes base.html)
    response = client.get(f'/pacientes/{paciente.id}/exames/', HTTP_ACCEPT='text/html')
    print(f"Response status: {response.status_code}")
    
    if response.status_code == 500:
        print("[ERROR] Server error 500")
        # Try to capture error details
        print(response.content[:1000])
    else:
        print("[OK] Page loaded successfully")
        # Check if the 'Meus Exames' link is present in rendered HTML
        content = response.content.decode('utf-8', errors='ignore')
        print(f"First 500 chars of content: {content[:500]}")
        if 'Meus Exames' in content:
            print("[OK] 'Meus Exames' link found in page")
        else:
            print("[WARNING] 'Meus Exames' link not found")
        # Check for reverse URL error messages
        if 'Reverse for' in content and 'not found' in content:
            print("[ERROR] Template contains reverse URL error!")
            # Extract error snippet
            import re
            errors = re.findall(r'Reverse for .*? not found', content)
            for err in errors:
                print(f"  - {err}")
    
    # Clean up
    paciente.delete()
    print("Cleaned up test paciente.")

def test_template_with_medico():
    print("\nTesting template rendering with médico user...")
    client = Client()
    
    unique_id = generate_random_string(6)
    email = f'test.medico.{unique_id}@example.com'
    cpf = generate_valid_cpf()
    password = 'testpassword123'
    
    from core.models import Medico
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
    
    client.login(username=email, password=password)
    
    # Debug: get user and check properties
    from django.contrib.auth import get_user_model
    User = get_user_model()
    user = User.objects.get(email=email)
    print(f"User ID: {user.id}")
    print(f"User is_paciente: {user.is_paciente}")
    print(f"User is_medico: {user.is_medico}")
    print(f"Hasattr medico: {hasattr(user, 'medico')}")
    if hasattr(user, 'medico'):
        print(f"Medico ID: {user.medico.id}")
    
    response = client.get(f'/medicos/{medico.id}/dashboard/')
    print(f"Response status: {response.status_code}")
    
    if response.status_code == 500:
        print("[ERROR] Server error 500")
        print(response.content[:1000])
    else:
        print("[OK] Page loaded successfully")
        content = response.content.decode('utf-8', errors='ignore')
        if 'Dashboard' in content:
            print("[OK] 'Dashboard' link found in page")
        else:
            print("[WARNING] 'Dashboard' link not found")
        if 'Reverse for' in content and 'not found' in content:
            print("[ERROR] Template contains reverse URL error!")
            import re
            errors = re.findall(r'Reverse for .*? not found', content)
            for err in errors:
                print(f"  - {err}")
    
    medico.delete()
    print("Cleaned up test médico.")

if __name__ == '__main__':
    test_template_with_paciente()
    test_template_with_medico()