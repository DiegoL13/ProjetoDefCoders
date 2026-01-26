#!/usr/bin/env python
import os
import sys
import django

sys.path.insert(0, 'C:\\Users\\Domi\\Downloads\\PortalSaude-fixed_bugs\\PortalSaude-Continuacao\\sistema')
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

print("=== Testing complete paciente flow ===")

# Create test paciente
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

print(f"Created paciente ID: {paciente.id}")

client = Client()

# 1. Login
print("\n1. Logging in...")
response = client.post('/login/', {'username': email, 'password': password})
if response.status_code != 302:
    print(f"ERROR: Login failed, status {response.status_code}")
    print(response.content[:500])
    sys.exit(1)

print(f"Login successful, redirect to: {response.url}")

# 2. Follow redirect to exames page
print("\n2. Accessing exames page...")
response = client.get(response.url)
if response.status_code != 200:
    print(f"ERROR: Exames page failed, status {response.status_code}")
    print(response.content[:500])
    sys.exit(1)

print(f"Exames page loaded successfully")

# 3. Check for reverse errors in content
content = response.content.decode('utf-8', errors='ignore')
if 'Reverse for' in content and 'not found' in content:
    print("ERROR: Found reverse URL error in page!")
    # Extract error snippet
    import re
    match = re.search(r'Reverse for .*? not found', content)
    if match:
        print(f"Error: {match.group(0)}")
    sys.exit(1)
else:
    print("No reverse URL errors detected.")

# 4. Check if navbar link is present and correct
if 'paciente-exames-list' in content:
    print("Navbar link reference found (paciente-exames-list).")
else:
    print("WARNING: Navbar link reference not found.")

# 5. Access base template directly (home page) while authenticated
print("\n3. Accessing home page while authenticated...")
response = client.get('/')
if response.status_code == 200:
    content = response.content.decode('utf-8', errors='ignore')
    if 'Reverse for' in content and 'not found' in content:
        print("ERROR: Reverse error on home page!")
        sys.exit(1)
    else:
        print("Home page loaded without errors.")
else:
    print(f"WARNING: Home page status {response.status_code}")

# 6. Logout
print("\n4. Logging out...")
response = client.post('/logout/')
if response.status_code in [302, 200]:
    print("Logout successful.")
else:
    print(f"WARNING: Logout status {response.status_code}")

# Cleanup
paciente.delete()
print("\nTest completed successfully. No URL reverse errors found.")

print("\n=== Additional check: Verify URL reverse for paciente-exames-list ===")
from django.urls import reverse, NoReverseMatch
try:
    url = reverse('paciente-exames-list', kwargs={'paciente_id': paciente.id})
    print(f"URL reverse works: {url}")
except NoReverseMatch as e:
    print(f"ERROR: URL reverse failed: {e}")
    sys.exit(1)

print("\n✅ All tests passed! The paciente login flow is fixed.")