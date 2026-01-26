#!/usr/bin/env python
import os
import sys
import django

sys.path.insert(0, 'C:\\Users\\Domi\\Downloads\\PortalSaude-fixed_bugs\\PortalSaude-Continuacao\\sistema')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema.settings')

django.setup()

from django.urls import reverse, NoReverseMatch

# Testar todas as variações possíveis
url_names_to_test = [
    'paciente-exames',  # Basename sem sufixo
    'paciente-exames-list',
    'paciente-exames-detail',
    'medico-exames',    # Basename sem sufixo  
    'medico-exames-list',
    'medico-exames-detail',
]

print("Testing URL reverses for paciente/medico exames...")
for name in url_names_to_test:
    try:
        if 'paciente' in name:
            if 'detail' in name:
                # Para detail precisa de paciente_id e pk
                url = reverse(name, kwargs={'paciente_id': 1, 'pk': 1})
            else:
                url = reverse(name, kwargs={'paciente_id': 1})
        elif 'medico' in name:
            if 'detail' in name:
                # Para detail precisa de medico_id e pk
                url = reverse(name, kwargs={'medico_id': 1, 'pk': 1})
            else:
                url = reverse(name, kwargs={'medico_id': 1})
        else:
            url = reverse(name)
        print(f"[OK] {name} -> {url}")
    except NoReverseMatch as e:
        print(f"[ERROR] {name} -> ERROR: {e}")

# Testar também reverse sem kwargs para ver mensagem de erro
print("\nTesting without required kwargs...")
try:
    url = reverse('paciente-exames-list')
except NoReverseMatch as e:
    print(f"Expected error for paciente-exames-list without kwargs: {e}")

try:
    url = reverse('paciente-exames')
except NoReverseMatch as e:
    print(f"Error for paciente-exames (basename): {e}")