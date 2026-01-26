#!/usr/bin/env python3
"""
Test patient and doctor registration forms.
"""
import requests
import re
import sys
import random

BASE_URL = "http://127.0.0.1:8000"
SESSION = requests.Session()

def generate_valid_cpf():
    """Generate a random valid CPF (Brazilian ID)."""
    # Generate 9 random digits
    digits = [random.randint(0, 9) for _ in range(9)]
    # Calculate first check digit
    sum1 = sum(digits[i] * (10 - i) for i in range(9))
    resto1 = sum1 % 11
    digit1 = 0 if resto1 < 2 else 11 - resto1
    digits.append(digit1)
    # Calculate second check digit
    sum2 = sum(digits[i] * (11 - i) for i in range(10))
    resto2 = sum2 % 11
    digit2 = 0 if resto2 < 2 else 11 - resto2
    digits.append(digit2)
    # Convert to string
    cpf = ''.join(str(d) for d in digits)
    return cpf

def get_csrf_token(url):
    """Extract CSRF token from a Django form page."""
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

def test_patient_registration():
    """Test patient registration."""
    print("\n=== Testing Patient Registration ===")
    url = f"{BASE_URL}/cadastro/paciente/"
    
    # Get CSRF token
    csrf_token = get_csrf_token(url)
    print(f"CSRF token obtained")
    
    # Generate unique email
    random_id = random.randint(1000, 9999)
    email = f"test.patient.{random_id}@example.com"
    
    # Generate valid CPF that hopefully not in use
    valid_cpf = generate_valid_cpf()
    print(f"Generated CPF: {valid_cpf}")
    
    data = {
        'csrfmiddlewaretoken': csrf_token,
        'nome': 'Test Patient',
        'email': email,
        'password': 'TestPassword123',
        'confirm_password': 'TestPassword123',
        'cpf': valid_cpf,
        'data_nascimento': '1990-01-01',
        'sexo': 'feminino',
        'contato': '11999999999',
        'historico_medico': '',
    }
    
    headers = {
        'Referer': url
    }
    
    response = SESSION.post(url, data=data, headers=headers, allow_redirects=False)
    print(f"Status code: {response.status_code}")
    if response.status_code == 302:
        redirect = response.headers.get('Location', '')
        print(f"Redirect to: {redirect}")
        print("Patient registration successful!")
        return True
    else:
        print(f"Registration failed. Response text (first 500 chars): {response.text[:500]}")
        # Extract form errors
        error_pattern = r'<div class="invalid-feedback">([^<]+)</div>'
        errors = re.findall(error_pattern, response.text)
        if errors:
            print(f"Form errors: {errors}")
        # Also look for error list
        if 'error' in response.text.lower() or 'invalid' in response.text.lower():
            print("Errors found in response.")
        return False

def test_doctor_registration():
    """Test doctor registration."""
    print("\n=== Testing Doctor Registration ===")
    url = f"{BASE_URL}/cadastro/medico/"
    
    csrf_token = get_csrf_token(url)
    print(f"CSRF token obtained")
    
    random_id = random.randint(1000, 9999)
    email = f"test.doctor.{random_id}@example.com"
    
    # Generate valid CPF
    valid_cpf = generate_valid_cpf()
    print(f"Generated CPF: {valid_cpf}")
    
    data = {
        'csrfmiddlewaretoken': csrf_token,
        'nome': 'Dr. Test Doctor',
        'email': email,
        'password': 'TestPassword123',
        'confirm_password': 'TestPassword123',
        'cpf': valid_cpf,
        'crm': f'CRM-SP-{random_id}',
        'especialidade': 'Cardiology',
        'contato': '11888888888',
        'data_nascimento': '1980-05-15',
        'sexo': 'masculino',
    }
    
    headers = {
        'Referer': url
    }
    
    response = SESSION.post(url, data=data, headers=headers, allow_redirects=False)
    print(f"Status code: {response.status_code}")
    if response.status_code == 302:
        redirect = response.headers.get('Location', '')
        print(f"Redirect to: {redirect}")
        print("Doctor registration successful!")
        return True
    else:
        print(f"Registration failed. Response text (first 500 chars): {response.text[:500]}")
        # Extract form errors
        error_pattern = r'<div class="invalid-feedback">([^<]+)</div>'
        errors = re.findall(error_pattern, response.text)
        if errors:
            print(f"Form errors: {errors}")
        if 'error' in response.text.lower() or 'invalid' in response.text.lower():
            print("Errors found in response.")
        return False

def main():
    print("Starting registration tests...")
    success = True
    
    if not test_patient_registration():
        success = False
    
    # Clear cookies for next test
    SESSION.cookies.clear()
    
    if not test_doctor_registration():
        success = False
    
    if success:
        print("\nAll registration tests passed!")
        return 0
    else:
        print("\nSome registration tests failed.")
        return 1

if __name__ == "__main__":
    sys.exit(main())