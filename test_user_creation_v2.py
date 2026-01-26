#!/usr/bin/env python
import os
import sys
import django

# Adicionar o diretório do projeto ao path
sys.path.insert(0, 'C:\\Users\\Domi\\Downloads\\PortalSaude-fixed_bugs\\PortalSaude-Continuacao\\sistema')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema.settings')

django.setup()

from core.models import Medico, Paciente, Usuario

print("=== TESTANDO CRIAÇÃO DE USUÁRIOS ===")

# Usar emails únicos
import random
unique_id = random.randint(1000, 9999)

# Teste 1: Criar médico
print("\n1. Testando criação de médico...")
try:
    medico_data = {
        'nome': f'Dr. Teste Médico {unique_id}',
        'email': f'test.medico.{unique_id}@example.com',
        'password': 'testpassword123',
        'cpf': f'12345678{str(unique_id).zfill(3)}',
        'crm': f'CRM-SP-{unique_id}',
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
    
    print(f"SUCESSO: Médico criado! ID: {medico.id}")
    
    # Verificar persistência no banco
    medico_db = Medico.objects.get(email=medico_data['email'])
    print(f"SUCESSO: Médico confirmado no banco! ID no banco: {medico_db.id}")
    print(f"   CPF: {medico_db.cpf}")
    print(f"   CRM: {medico_db.crm}")
    
except Exception as e:
    print(f"ERRO: Ao criar médico: {e}")

# Teste 2: Verificar herança multi-tabela
print("\n2. Testando herança multi-tabela...")
try:
    usuario_base = Usuario.objects.get(email=f'test.medico.{unique_id}@example.com')
    print(f"SUCESSO: Usuário base encontrado! ID: {usuario_base.id}")
    print(f"   Email: {usuario_base.email}")
    print(f"   Nome: {usuario_base.nome}")
    
    medico_relacionado = Medico.objects.get(usuario_ptr_id=usuario_base.id)
    print(f"SUCESSO: Médico relacionado encontrado! ID: {medico_relacionado.id}")
    print(f"   CRM: {medico_relacionado.crm}")
    
    print(f"Relação: Usuario ({usuario_base.id}) <-> Medico ({medico_relacionado.id})")
    
except Exception as e:
    print(f"ERRO: Na verificação de herança: {e}")

# Teste 3: Testar autenticação
print("\n3. Testando autenticação...")
try:
    from django.contrib.auth import authenticate
    
    # Autenticar usuário
    user = authenticate(email=f'test.medico.{unique_id}@example.com', password='testpassword123')
    if user is not None:
        print(f"SUCESSO: Autenticação bem-sucedida!")
        print(f"   Usuário autenticado: {user.email}")
        
        # Testar hasattr vs consulta direta
        print(f"   Teste hasattr(user, 'medico'): {hasattr(user, 'medico')}")
        
        # Testar consulta EXPLÍCITA ao banco
        try:
            medico_from_db = Medico.objects.get(usuario_ptr_id=user.id)
            print(f"   Consulta explícita ao banco: ENCONTRADO (ID: {medico_from_db.id})")
            
        except Medico.DoesNotExist:
            print(f"   Consulta explícita ao banco: NÃO ENCONTRADO")
            
    else:
        print(f"ERRO: Falha na autenticação")
        
except Exception as e:
    print(f"ERRO: Na autenticação: {e}")

print("\n=== TESTE CONCLUÍDO ===")