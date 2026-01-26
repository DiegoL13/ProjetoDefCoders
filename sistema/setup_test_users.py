import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema.settings')
django.setup()

from core.models import Usuario, Medico, Paciente
from django.db import transaction

print("=== Setting up test users ===")

# Common password for all test users
TEST_PASSWORD = 'password'

def ensure_user(email, nome, cpf, is_medico=False, is_paciente=False, **extra_fields):
    """Ensure a user exists with given profile"""
    try:
        user = Usuario.objects.get(email=email)
        print(f"[OK] User {email} already exists")
        # Update password
        user.set_password(TEST_PASSWORD)
        user.save()
    except Usuario.DoesNotExist:
        # Create appropriate user type
        common_fields = dict(
            email=email,
            nome=nome,
            cpf=cpf,
            data_nascimento='1990-01-01',
            sexo='masculino',
            contato='11999999999',
            **extra_fields
        )
        
        if is_medico:
            user = Medico(**common_fields)
            user.crm = f'CRM-SP-{cpf}'
            user.especialidade = 'Radiologia'
        elif is_paciente:
            user = Paciente(**common_fields)
            user.historico_medico = 'Nenhum historico significativo'
        else:
            user = Usuario(**common_fields)
        
        user.set_password(TEST_PASSWORD)
        user.save()
        print(f"[OK] Created user {email}")
    
    # Ensure profiles (for existing users that might not have profile)
    if is_medico and not hasattr(user, 'medico'):
        # Convert existing Usuario to Medico
        medico = Medico(usuario_ptr=user, crm=f'CRM-SP-{user.cpf}', especialidade='Radiologia')
        medico.save()
        print(f"[OK] Created medico profile for {email}")
    
    if is_paciente and not hasattr(user, 'paciente'):
        paciente = Paciente(usuario_ptr=user, historico_medico='Nenhum historico significativo')
        paciente.save()
        print(f"[OK] Created paciente profile for {email}")
    
    return user

# Main execution
with transaction.atomic():
    # Doctor users
    doctor1 = ensure_user(
        email='doctor@example.com',
        nome='Dr. Test Doctor',
        cpf='11122233344',
        is_medico=True
    )
    
    doctor2 = ensure_user(
        email='medico@example.com',
        nome='Dr. Teste Medico',
        cpf='22233344455',
        is_medico=True
    )
    
    # Patient users
    patient1 = ensure_user(
        email='patient@example.com',
        nome='Test Patient',
        cpf='11122233345',
        is_paciente=True
    )
    
    patient2 = ensure_user(
        email='paciente@example.com',
        nome='Maria Santos',
        cpf='44455566677',
        is_paciente=True
    )
    
    # Additional test users from README
    doctor3 = ensure_user(
        email='test.medico@example.com',
        nome='Dr. Test Doctor User',
        cpf='55566677788',
        is_medico=True
    )
    
    patient3 = ensure_user(
        email='test.paciente@example.com',
        nome='Test Patient User',
        cpf='66677788899',
        is_paciente=True
    )

print("\n=== User IDs ===")
for email in ['doctor@example.com', 'medico@example.com', 'patient@example.com', 'paciente@example.com']:
    try:
        user = Usuario.objects.get(email=email)
        profile_type = 'medico' if hasattr(user, 'medico') else 'paciente' if hasattr(user, 'paciente') else 'none'
        profile_id = user.medico.id if hasattr(user, 'medico') else user.paciente.id if hasattr(user, 'paciente') else 'N/A'
        print(f"{email}: User ID {user.id}, {profile_type} ID {profile_id}")
    except Usuario.DoesNotExist:
        print(f"{email}: Not found")

print("\n[OK] All test users set up with password 'password'")