import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema.settings')
django.setup()

from core.models import Usuario as User

# Reset passwords for test users
test_users = [
    ('medico@example.com', 'password'),
    ('paciente@example.com', 'password'),
    ('js.fer@gmail.com', 'password'),
    ('final.medico@example.com', 'password'),
    ('final.paciente@example.com', 'password'),
    ('pedro@example.com', 'password'),
    ('teste.medico@exemplo.com', 'password'),
]

for email, password in test_users:
    try:
        user = User.objects.get(email=email)
        user.set_password(password)
        user.save()
        print(f'Password reset for {email}')
    except User.DoesNotExist:
        print(f'User {email} not found')

# Also create doctor@example.com and patient@example.com if they don't exist
new_users = [
    ('doctor@example.com', 'password', 'Dr. Test Doctor'),
    ('patient@example.com', 'password', 'Test Patient'),
]

for email, password, name in new_users:
    if not User.objects.filter(email=email).exists():
        user = User.objects.create_user(
            email=email,
            password=password,
            nome=name,
            cpf='11122233344',  # Placeholder CPF
            data_nascimento='1990-01-01',
            sexo='masculino',
            contato='11999999999'
        )
        print(f'Created user {email}')
    else:
        print(f'User {email} already exists')

print('\nAll passwords have been reset to "password"')