#!/usr/bin/env python
import os
import sys
import django
import random
import string

# Adicionar o diretório do projeto ao path
sys.path.insert(0, 'C:\\Users\\Domi\\Downloads\\PortalSaude-fixed_bugs\\PortalSaude-Continuacao\\sistema')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema.settings')

django.setup()

from core.models import Medico, Paciente, Usuario
from core.forms import MedicoCreationForm, PacienteCreationForm

def generate_random_email():
    random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f'test.medico.{random_str}@example.com'

print("=== TESTANDO CRIAÇÃO DE USUÁRIOS ===")

# Gerar email único
test_email = generate_random_email()
test_cpf = '12345678901'
print(f"Usando email de teste: {test_email}")
print(f"Usando CPF de teste: {test_cpf}")

# Limpar dados de teste anteriores (com segurança)
try:
    Medico.objects.filter(cpf=test_cpf).delete()
    Usuario.objects.filter(email=test_email).delete()
    print("[INFO] Dados de teste anteriores removidos.")
except Exception as e:
    print(f"[INFO] Nenhum dado anterior para limpar ou erro: {e}")

# Teste 1: Criar médico
print("\n1. Testando criação de médico...")
try:
    medico_data = {
        'nome': 'Dr. Teste Médico',
        'email': test_email,
        'password': 'testpassword123',
        'cpf': test_cpf,
        'crm': 'CRM-SP-999888777',
        'especialidade': 'Cardiologia',
        'data_nascimento': '1980-01-01',
        'sexo': 'masculino',
        'contato': '(11) 99999-8888'
    }
    
    # Criar usando o model diretamente
    from django.db import transaction
    with transaction.atomic():
        medico = Medico.objects.create_user(
            email=medico_data['email'],
            password=medico_data['password'],
            nome=medico_data['nome'],
            cpf=medico_data['cpf'],
            crm=medico_data['crm'],
            especialidade=medico_data['especialidade'],
            data_nascimento=medico_data['data_nascimento'],
            sexo=medico_data['sexo'],
            contato=medico_data['contato']
        )
    
    print(f"[OK] Médico criado com sucesso! ID: {medico.id}")
    
    # Verificar persistência no banco
    medico_db = Medico.objects.get(email=medico_data['email'])
    print(f"[OK] Médico confirmado no banco! ID no banco: {medico_db.id}")
    print(f"   CPF: {medico_db.cpf}")
    print(f"   CRM: {medico_db.crm}")
    
except Exception as e:
    print(f"[ERRO] Erro ao criar médico: {e}")

# Teste 2: Verificar herança multi-tabela
print("\n2. Testando herança multi-tabela...")
try:
    usuario_base = Usuario.objects.get(email=test_email)
    print(f"[OK] Usuário base encontrado! ID: {usuario_base.id}")
    
    medico_relacionado = Medico.objects.get(usuario_ptr_id=usuario_base.id)
    print(f"[OK] Médico relacionado encontrado! ID: {medico_relacionado.id}")
    
    print(f"   Relação: Usuario ({usuario_base.id}) <-> Medico ({medico_relacionado.id})")
    
except Exception as e:
    print(f"[ERRO] Erro na verificação de herança: {e}")

print("\n=== TESTE CONCLUÍDO ===")