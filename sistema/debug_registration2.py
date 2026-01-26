#!/usr/bin/env python3
import requests
import re
import random

def generate_valid_cpf():
    digits = [random.randint(0, 9) for _ in range(9)]
    sum1 = sum(digits[i] * (10 - i) for i in range(9))
    resto1 = sum1 % 11
    digit1 = 0 if resto1 < 2 else 11 - resto1
    digits.append(digit1)
    sum2 = sum(digits[i] * (11 - i) for i in range(10))
    resto2 = sum2 % 11
    digit2 = 0 if resto2 < 2 else 11 - resto2
    digits.append(digit2)
    return ''.join(str(d) for d in digits)

BASE_URL = "http://127.0.0.1:8000"
SESSION = requests.Session()

def get_csrf_token(url):
    response = SESSION.get(url)
    response.raise_for_status()
    match = re.search(r"name='csrfmiddlewaretoken' value='([^']+)'", response.text)
    if match:
        return match.group(1)
    else:
        match = re.search(r'csrfmiddlewaretoken" value="([^"]+)"', response.text)
        if match:
            return match.group(1)
    raise ValueError("CSRF token not found")

print("=== Testing Patient Registration with generated CPF ===")
url = f"{BASE_URL}/cadastro/paciente/"
csrf = get_csrf_token(url)
cpf = generate_valid_cpf()
print(f"CPF: {cpf}")

data = {
    'csrfmiddlewaretoken': csrf,
    'nome': 'Test Patient',
    'email': f'test.patient.{random.randint(1000,9999)}@example.com',
    'password': 'TestPassword123',
    'confirm_password': 'TestPassword123',
    'cpf': cpf,
    'data_nascimento': '1990-01-01',
    'sexo': 'feminino',
    'contato': '11999999999',
    'historico_medico': '',
}

headers = {'Referer': url}
response = SESSION.post(url, data=data, headers=headers, allow_redirects=False)
print(f"Status: {response.status_code}")
if response.status_code == 302:
    print("SUCCESS: Redirect to", response.headers.get('Location'))
else:
    print("FAILED")
    # Check if FieldError in response
    if 'FieldError' in response.text:
        print("FieldError detected")
        # Extract traceback
        import re
        tb = re.search(r'<pre class="exception_value">(.*?)</pre>', response.text, re.DOTALL)
        if tb:
            print("Exception:", tb.group(1))
    # Print first 3000 chars
    print(response.text[:3000])