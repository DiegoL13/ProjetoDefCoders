#!/usr/bin/env python
import subprocess
import time
import sys
import os
import requests
from requests.exceptions import RequestException
import random
import string

def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def generate_random_cpf():
    # Generate a valid CPF using the same algorithm as forms.py
    import random
    # Generate first 9 digits
    digits = [random.randint(0, 9) for _ in range(9)]
    
    # Calculate first check digit
    soma = 0
    for i in range(9):
        soma += digits[i] * (10 - i)
    resto = soma % 11
    digito1 = 0 if resto < 2 else 11 - resto
    digits.append(digito1)
    
    # Calculate second check digit
    soma = 0
    for i in range(10):
        soma += digits[i] * (11 - i)
    resto = soma % 11
    digito2 = 0 if resto < 2 else 11 - resto
    digits.append(digito2)
    
    # Ensure not all digits are the same (invalid CPF)
    if all(d == digits[0] for d in digits):
        # Fallback to a known valid CPF
        return '52998224725'
    
    return ''.join(str(d) for d in digits)

def start_server():
    os.chdir('sistema')
    server = subprocess.Popen(
        [sys.executable, 'manage.py', 'runserver', '127.0.0.1:8000', '--noreload'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    time.sleep(8)
    return server

def get_csrf_token(session, url):
    response = session.get(url)
    # Extract CSRF token from HTML
    import re
    # Look for <input type="hidden" name="csrfmiddlewaretoken" value="...">
    match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', response.text)
    if match:
        return match.group(1)
    else:
        raise ValueError('CSRF token not found')

def test_medico_registration():
    print('Testing médico registration...')
    base_url = 'http://127.0.0.1:8000'
    session = requests.Session()
    
    # Get the registration page
    reg_url = base_url + '/cadastro/medico/'
    try:
        csrf_token = get_csrf_token(session, reg_url)
    except ValueError as e:
        print(f'[ERROR] Failed to get CSRF token: {e}')
        return False
    
    # Generate unique data
    unique_id = generate_random_string(6)
    email = f'test.medico.{unique_id}@example.com'
    cpf = generate_random_cpf()
    
    # Prepare form data
    form_data = {
        'csrfmiddlewaretoken': csrf_token,
        'nome': f'Dr. Teste Médico {unique_id}',
        'email': email,
        'password': 'testpassword123',
        'confirm_password': 'testpassword123',
        'cpf': cpf,
        'crm': f'CRM-SP-{unique_id}',
        'especialidade': 'Cardiologia',
        'data_nascimento': '1980-01-01',
        'sexo': 'masculino',
        'contato': '(11) 99999-8888',
    }
    
    # Submit POST
    headers = {'Referer': reg_url}
    try:
        response = session.post(reg_url, data=form_data, headers=headers, allow_redirects=False)
        # Expect redirect to dashboard (status 302) or 200 with success
        print(f'Response status: {response.status_code}')
        if response.status_code in (200, 302):
            print('[OK] Médico registration submission successful')
            # Check if redirect location contains medico dashboard
            if response.status_code == 302:
                location = response.headers.get('Location', '')
                print(f'Redirect to: {location}')
                if '/medicos/' in location and '/dashboard/' in location:
                    print('[OK] Redirected to médico dashboard')
                    return True
                else:
                    print('[WARNING] Unexpected redirect location')
            else:
                # Maybe form errors displayed, check for error messages
                if 'error' in response.text.lower() or 'invalid' in response.text.lower():
                    print('[ERROR] Form errors detected')
                    # Print snippet of response for debugging
                    print(response.text[:500])
                    return False
                else:
                    print('[OK] Registration likely succeeded (no redirect)')
                    return True
        else:
            print(f'[ERROR] Unexpected status code: {response.status_code}')
            print(response.text[:500])
            return False
    except RequestException as e:
        print(f'[ERROR] Request failed: {e}')
        return False

def test_paciente_registration():
    print('Testing paciente registration...')
    base_url = 'http://127.0.0.1:8000'
    session = requests.Session()
    
    reg_url = base_url + '/cadastro/paciente/'
    try:
        csrf_token = get_csrf_token(session, reg_url)
    except ValueError as e:
        print(f'[ERROR] Failed to get CSRF token: {e}')
        return False
    
    unique_id = generate_random_string(6)
    email = f'test.paciente.{unique_id}@example.com'
    cpf = generate_random_cpf()
    
    form_data = {
        'csrfmiddlewaretoken': csrf_token,
        'nome': f'Paciente Teste {unique_id}',
        'email': email,
        'password': 'testpassword123',
        'confirm_password': 'testpassword123',
        'cpf': cpf,
        'data_nascimento': '1990-05-15',
        'sexo': 'feminino',
        'contato': '(11) 98888-7777',
        'historico_medico': 'Nenhum',
    }
    
    headers = {'Referer': reg_url}
    try:
        response = session.post(reg_url, data=form_data, headers=headers, allow_redirects=False)
        print(f'Response status: {response.status_code}')
        if response.status_code in (200, 302):
            print('[OK] Paciente registration submission successful')
            if response.status_code == 302:
                location = response.headers.get('Location', '')
                print(f'Redirect to: {location}')
                if '/pacientes/' in location and '/exames/' in location:
                    print('[OK] Redirected to paciente exames')
                    return True
                else:
                    print('[WARNING] Unexpected redirect location')
            else:
                if 'error' in response.text.lower() or 'invalid' in response.text.lower():
                    print('[ERROR] Form errors detected')
                    print(response.text[:500])
                    return False
                else:
                    print('[OK] Registration likely succeeded')
                    return True
        else:
            print(f'[ERROR] Unexpected status code: {response.status_code}')
            print(response.text[:500])
            return False
    except RequestException as e:
        print(f'[ERROR] Request failed: {e}')
        return False

def main():
    print('Starting Django server for form submission tests...')
    server = start_server()
    
    try:
        success_medico = test_medico_registration()
        success_paciente = test_paciente_registration()
        
        if success_medico and success_paciente:
            print('\n[SUCCESS] All form submission tests passed!')
        else:
            print('\n[FAILURE] Some form submission tests failed.')
            sys.exit(1)
    finally:
        print('Stopping server...')
        server.terminate()
        server.wait()
        print('Server stopped.')

if __name__ == '__main__':
    main()