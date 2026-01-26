#!/usr/bin/env python3
import requests
import re

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

url = f"{BASE_URL}/cadastro/paciente/"
csrf = get_csrf_token(url)
print(f"CSRF: {csrf}")

data = {
    'csrfmiddlewaretoken': csrf,
    'nome': 'Test Patient',
    'email': 'test.patient.9999@example.com',
    'password': 'TestPassword123',
    'confirm_password': 'TestPassword123',
    'cpf': '12345678909',
    'data_nascimento': '1990-01-01',
    'sexo': 'feminino',
    'contato': '11999999999',
    'historico_medico': '',
}

headers = {'Referer': url}
response = SESSION.post(url, data=data, headers=headers, allow_redirects=False)
print(f"Status: {response.status_code}")
print(f"Headers: {response.headers}")
print(f"Response text (first 2000 chars):")
print(response.text[:2000])
print("\n--- Full response ---")
print(response.text)