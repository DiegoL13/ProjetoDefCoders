#!/usr/bin/env python3
"""
Create a test exam for doctor 23 and patient 24.
"""
import requests
import sys
import re

BASE_URL = "http://127.0.0.1:8000"
SESSION = requests.Session()

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

def login(username, password):
    """Login to the application."""
    login_url = f"{BASE_URL}/login/"
    csrf_token = get_csrf_token(login_url)
    
    data = {
        'csrfmiddlewaretoken': csrf_token,
        'username': username,
        'password': password,
    }
    
    response = SESSION.post(login_url, data=data, allow_redirects=False)
    if response.status_code == 302:
        redirect_url = response.headers.get('Location')
        print(f"Login successful for {username}. Redirected to: {redirect_url}")
        return redirect_url
    else:
        print(f"Login failed for {username}. Status: {response.status_code}")
        return None

def create_exam(medico_id, paciente_id, descricao="Test exam description"):
    """Create a new exam via the CriarExameView."""
    # First get the novo-exame page to obtain CSRF token
    novo_exame_url = f"{BASE_URL}/medicos/{medico_id}/novo-exame/"
    csrf_token = get_csrf_token(novo_exame_url)
    
    # Prepare form data
    data = {
        'csrfmiddlewaretoken': csrf_token,
        'paciente': paciente_id,
        'descricao': descricao,
        # No images for now
    }
    
    # No files
    files = {}
    
    response = SESSION.post(novo_exame_url, data=data, files=files)
    print(f"Create exam response status: {response.status_code}")
    print(f"Response JSON: {response.text}")
    return response.json()

def update_exam_disponibilidade(exame_id, disponibilidade=True):
    """Update exam disponibilidade via EditarExameView."""
    edit_url = f"{BASE_URL}/exame/{exame_id}/editar/"
    
    # Get CSRF token from cookie (already set by login)
    csrf_token = SESSION.cookies.get('csrftoken')
    if not csrf_token:
        # Fallback: get token from any page
        csrf_token = get_csrf_token(f"{BASE_URL}/medicos/23/dashboard/")
    
    # Prepare form data as the view expects
    # The view expects resultado_medico, disponibilidade, descricao, imagens_remover (list), novas_imagens (files)
    # We'll send minimal data
    data = {
        'csrfmiddlewaretoken': csrf_token,
        'resultado_medico': 'SAUDÁVEL',
        'disponibilidade': 'true' if disponibilidade else 'false',
        'descricao': 'Test exam updated via script',
        # imagens_remover as empty list - Django expects list with repeated keys
        # We can omit it, but to be safe we send empty
    }
    # For list fields, we need to send repeated keys; we'll skip for empty
    
    response = SESSION.post(edit_url, data=data)
    print(f"Update exam response status: {response.status_code}")
    print(f"Response JSON: {response.text}")
    return response.json()

def get_csrf_token_from_response(html):
    """Extract CSRF token from HTML response."""
    match = re.search(r"name='csrfmiddlewaretoken' value='([^']+)'", html)
    if match:
        return match.group(1)
    match = re.search(r'csrfmiddlewaretoken" value="([^"]+)"', html)
    if match:
        return match.group(1)
    raise ValueError("CSRF token not found")

def main():
    print("Creating test exam...")
    
    # Login as doctor
    login("doctor@example.com", "password")
    
    # Create exam for patient 24
    result = create_exam(medico_id=23, paciente_id=24, descricao="Test exam created via script")
    if result.get('success'):
        exame_id = result.get('exame_id')  # Does the response include exam ID? Not sure
        print(f"Exam created successfully. Need to extract exam ID from response.")
        # The response doesn't include exam ID, but we can get from redirect or query
        # For simplicity, we'll just note that exam was created
        # We can fetch the latest exam for doctor 23
        pass
    else:
        print(f"Failed to create exam: {result}")
        return 1
    
    # We can also test updating disponibilidade
    # But need exam ID; let's fetch doctor's exams to get the newly created exam
    exames_url = f"{BASE_URL}/medicos/23/exames/"
    response = SESSION.get(exames_url)
    if response.status_code == 200:
        exames = response.json()
        print(f"Doctor now has {len(exames)} exams")
        for exam in exames:
            print(f"  Exam ID: {exam['id']}, Patient: {exam['paciente_nome']}, Disponibilidade: {exam['disponibilidade']}")
            # Update the exam to make it available to patient
            if exam['id'] == 6:  # our newly created exam
                print(f"  Updating exam {exam['id']} disponibilidade to True...")
                update_exam_disponibilidade(exam['id'], True)
    
    print("\nTest completed.")
    return 0

if __name__ == "__main__":
    sys.exit(main())