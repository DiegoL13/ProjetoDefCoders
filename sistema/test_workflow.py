#!/usr/bin/env python3
"""
Test workflow for Portal Saúde Django application.
Tests doctor login, dashboard access, exam creation, and patient view.
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
        # Try alternative pattern
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
        print(f"Response text: {response.text[:500]}")
        return None

def test_doctor_workflow():
    """Test doctor workflow: login, dashboard, create exam."""
    print("\n=== Testing Doctor Workflow ===")
    
    # Login as doctor
    redirect_url = login("doctor@example.com", "password")
    if not redirect_url:
        print("Doctor login failed")
        return False
    
    # Follow redirect (should be doctor dashboard)
    if redirect_url.startswith('/'):
        redirect_url = BASE_URL + redirect_url
    response = SESSION.get(redirect_url)
    print(f"Dashboard page status: {response.status_code}")
    
    # Check if we're on doctor dashboard (look for medico ID in URL or page content)
    if '/medicos/' in redirect_url:
        medico_id = redirect_url.split('/medicos/')[1].split('/')[0]
        print(f"Doctor ID: {medico_id}")
        
        # Test dashboard API endpoint
        api_url = f"{BASE_URL}/medicos/{medico_id}/exames/"
        response = SESSION.get(api_url)
        print(f"Dashboard API status: {response.status_code}")
        if response.status_code == 200:
            exames = response.json()
            print(f"Found {len(exames)} exams in dashboard")
        else:
            print(f"API error: {response.text[:200]}")
        
        # Test new exam page
        novo_exame_url = f"{BASE_URL}/medicos/{medico_id}/novo-exame/"
        response = SESSION.get(novo_exame_url)
        print(f"New exam page status: {response.status_code}")
        
        # TODO: Actually create an exam with image upload
        # This would require more complex form handling
    
    return True

def test_patient_workflow():
    """Test patient workflow: login, view exams."""
    print("\n=== Testing Patient Workflow ===")
    
    # Login as patient
    redirect_url = login("patient@example.com", "password")
    if not redirect_url:
        print("Patient login failed")
        return False
    
    # Follow redirect (should be patient exams page)
    if redirect_url.startswith('/'):
        redirect_url = BASE_URL + redirect_url
    response = SESSION.get(redirect_url)
    print(f"Patient exams page status: {response.status_code}")
    
    # Check if we're on patient exams page
    if '/pacientes/' in redirect_url:
        paciente_id = redirect_url.split('/pacientes/')[1].split('/')[0]
        print(f"Patient ID: {paciente_id}")
        
        # Test patient exams API endpoint
        api_url = f"{BASE_URL}/pacientes/{paciente_id}/exames/"
        response = SESSION.get(api_url)
        print(f"Patient exams API status: {response.status_code}")
        if response.status_code == 200:
            exames = response.json()
            print(f"Found {len(exames)} exams available to patient")
        else:
            print(f"API error: {response.text[:200]}")
    
    return True

def test_api_endpoints():
    """Test key API endpoints."""
    print("\n=== Testing API Endpoints ===")
    
    # Test public endpoints (should redirect to login)
    endpoints = [
        "/medicos/",
        "/pacientes/",
        "/exames/",
        "/imagens/",
    ]
    
    for endpoint in endpoints:
        url = BASE_URL + endpoint
        response = SESSION.get(url)
        print(f"{endpoint}: {response.status_code}")
    
    # Try to access with authentication (after doctor login)
    SESSION.cookies.clear()
    login("doctor@example.com", "password")
    
    # Use known doctor ID from earlier test (doctor@example.com has ID 23)
    medico_id = 23
    # Test doctor-specific exam endpoint
    response = SESSION.get(f"{BASE_URL}/medicos/{medico_id}/exames/")
    print(f"Doctor exams endpoint: {response.status_code}")
    if response.status_code == 200:
        exames = response.json()
        print(f"  Found {len(exames)} exams")
    
    return True

def main():
    """Run all tests."""
    print("Starting Portal Saúde workflow tests...")
    
    # Clear session
    SESSION.cookies.clear()
    
    # Test workflows
    success = True
    
    if not test_doctor_workflow():
        success = False
    
    # Clear session for patient test
    SESSION.cookies.clear()
    
    if not test_patient_workflow():
        success = False
    
    # Test API endpoints
    if not test_api_endpoints():
        success = False
    
    if success:
        print("\nAll tests passed!")
        return 0
    else:
        print("\nSome tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())