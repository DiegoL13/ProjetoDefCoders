#!/usr/bin/env python
import os
import sys
import django

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'sistema'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema.settings')

django.setup()

from django.template import Template, Context
from django.test import RequestFactory
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

def test_template_rendering():
    print("Testing template rendering with mock user...")
    
    # Create a real paciente to get a real user object
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
    
    # Load base.html template
    template_path = os.path.join(os.path.dirname(__file__), 'sistema', 'core', 'templates', 'core', 'base.html')
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    template = Template(template_content)
    
    # Create a context with the user
    context = Context({'user': paciente})
    
    try:
        rendered = template.render(context)
        print("[SUCCESS] Template rendered without errors")
        # Check if the link is present
        if f'/pacientes/{paciente.id}/exames/' in rendered:
            print("[SUCCESS] Correct link found in rendered output")
        else:
            print("[WARNING] Link not found in output")
    except Exception as e:
        print(f"[ERROR] Template rendering failed: {e}")
        import traceback
        traceback.print_exc()
    
    # Clean up
    paciente.delete()
    print("Cleaned up test paciente.")

def test_template_with_medico():
    print("\nTesting template rendering with médico mock...")
    from core.models import Medico
    
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
    
    template_path = os.path.join(os.path.dirname(__file__), 'sistema', 'core', 'templates', 'core', 'base.html')
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    template = Template(template_content)
    context = Context({'user': medico})
    
    try:
        rendered = template.render(context)
        print("[SUCCESS] Template rendered without errors")
        if f'/medicos/{medico.id}/dashboard/' in rendered:
            print("[SUCCESS] Correct link found in rendered output")
        else:
            print("[WARNING] Link not found in output")
    except Exception as e:
        print(f"[ERROR] Template rendering failed: {e}")
        import traceback
        traceback.print_exc()
    
    medico.delete()
    print("Cleaned up test médico.")

if __name__ == '__main__':
    test_template_rendering()
    test_template_with_medico()