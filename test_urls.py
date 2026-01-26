#!/usr/bin/env python
import os
import sys
import django

sys.path.insert(0, 'C:\\Users\\Domi\\Downloads\\PortalSaude-fixed_bugs\\PortalSaude-Continuacao\\sistema')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema.settings')

django.setup()

from django.urls import reverse, NoReverseMatch

url_names = [
    'paciente-exames-list',
    'medico-dashboard',
    'cadastro_paciente',
    'cadastro_medico',
    'login',
    'logout',
    'home',
    'criar-exame',
    'editar-exame',
]

print("Testing URL reverses...")
for name in url_names:
    try:
        if name in ['paciente-exames-list', 'medico-dashboard']:
            # These need kwargs
            if name == 'paciente-exames-list':
                url = reverse(name, kwargs={'paciente_id': 1})
            else:
                url = reverse(name, kwargs={'medico_id': 1})
        elif name == 'editar-exame':
            url = reverse(name, kwargs={'exame_id': 1})
        else:
            url = reverse(name)
        print(f"[OK] {name} -> {url}")
    except NoReverseMatch as e:
        print(f"[ERROR] {name} -> ERROR: {e}")

# Also test the DRF router-generated names
print("\nTesting DRF router-generated names...")
router_names = [
    'paciente-exames-list',
    'paciente-exames-detail',
    'medico-exames-list',
    'medico-exames-detail',
]
for name in router_names:
    try:
        if 'paciente' in name:
            url = reverse(name, kwargs={'paciente_id': 1})
        elif 'medico' in name:
            url = reverse(name, kwargs={'medico_id': 1})
        else:
            url = reverse(name)
        print(f"[OK] {name} -> {url}")
    except NoReverseMatch as e:
        print(f"[ERROR] {name} -> ERROR: {e}")