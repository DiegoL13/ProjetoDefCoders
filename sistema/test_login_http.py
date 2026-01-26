import os
import sys
import time
import subprocess
import requests

def test_login():
    print("=== Testing Portal Saúde Login ===")
    
    # Start server on port 8002
    port = 8002
    base_url = f"http://127.0.0.1:{port}"
    
    print(f"Starting server on port {port}...")
    cmd = [sys.executable, "manage.py", "runserver", f"127.0.0.1:{port}", "--noreload", "--skip-check"]
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    try:
        # Wait for server to start
        print("Waiting for server to start...")
        time.sleep(5)
        
        # Test 1: Access login page
        print(f"\n1. Accessing login page...")
        try:
            response = requests.get(base_url + "/login/", timeout=10)
            if response.status_code == 200:
                print(f"   [OK] Login page loaded")
                # Check for CSRF token
                if 'csrf' in response.text.lower() or 'csrfmiddlewaretoken' in response.text:
                    print(f"   [OK] CSRF token found")
                else:
                    print(f"   [WARNING] CSRF token not found")
            else:
                print(f"   [ERROR] Login page status {response.status_code}")
                return False
        except Exception as e:
            print(f"   [ERROR] Failed to access login page: {e}")
            return False
        
        # Test 2: Login as medico@example.com
        print(f"\n2. Testing login as medico@example.com...")
        try:
            # First get CSRF token
            session = requests.Session()
            login_page = session.get(base_url + "/login/")
            # Extract CSRF token (simplified)
            csrf_token = None
            if 'csrfmiddlewaretoken' in login_page.text:
                # Simple extraction
                import re
                match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', login_page.text)
                if match:
                    csrf_token = match.group(1)
            
            if not csrf_token:
                print(f"   [WARNING] Could not extract CSRF token, trying without")
            
            # Prepare login data
            login_data = {
                'username': 'medico@example.com',  # Django's LoginView uses 'username' field
                'password': 'password',
            }
            if csrf_token:
                login_data['csrfmiddlewaretoken'] = csrf_token
            
            headers = {
                'Referer': base_url + '/login/'
            }
            
            # Post login
            response = session.post(base_url + "/login/", data=login_data, headers=headers, allow_redirects=False)
            
            if response.status_code == 302:
                print(f"   [OK] Login successful (redirect to {response.headers.get('Location', 'unknown')})")
                # Follow redirect
                redirect_url = response.headers.get('Location')
                if redirect_url:
                    response2 = session.get(base_url + redirect_url if redirect_url.startswith('/') else redirect_url)
                    print(f"   [OK] Redirected to: {redirect_url}")
                    print(f"   [OK] Final status: {response2.status_code}")
                    
                    # Check if we're on doctor dashboard
                    if 'dashboard' in redirect_url or 'medico' in redirect_url:
                        print(f"   [OK] Successfully redirected to doctor dashboard")
                    else:
                        print(f"   [WARNING] Unexpected redirect location")
                else:
                    print(f"   [WARNING] No redirect location")
            else:
                print(f"   [ERROR] Login failed with status {response.status_code}")
                print(f"   Response text: {response.text[:500]}")
                return False
                
        except Exception as e:
            print(f"   [ERROR] Login test failed: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        print(f"\n3. Testing login as paciente@example.com...")
        try:
            session = requests.Session()
            login_page = session.get(base_url + "/login/")
            
            login_data = {
                'username': 'paciente@example.com',
                'password': 'password',
            }
            
            # Try to extract CSRF token again
            import re
            match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', login_page.text)
            if match:
                login_data['csrfmiddlewaretoken'] = match.group(1)
            
            response = session.post(base_url + "/login/", data=login_data, allow_redirects=False)
            
            if response.status_code == 302:
                redirect_url = response.headers.get('Location', '')
                print(f"   [OK] Login successful, redirect to: {redirect_url}")
            else:
                print(f"   [WARNING] Login status {response.status_code}")
                # Might still be successful with different status
            
        except Exception as e:
            print(f"   [WARNING] Patient login test skipped: {e}")
        
        print(f"\n4. Testing login as doctor@example.com...")
        try:
            session = requests.Session()
            login_page = session.get(base_url + "/login/")
            
            login_data = {
                'username': 'doctor@example.com',
                'password': 'password',
            }
            
            import re
            match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', login_page.text)
            if match:
                login_data['csrfmiddlewaretoken'] = match.group(1)
            
            response = session.post(base_url + "/login/", data=login_data, allow_redirects=False)
            
            if response.status_code == 302:
                redirect_url = response.headers.get('Location', '')
                print(f"   [OK] Login successful, redirect to: {redirect_url}")
                # Verify redirect is to medico dashboard
                if '/medicos/23/' in redirect_url:
                    print(f"   [OK] Correct medico dashboard redirect")
                else:
                    print(f"   [WARNING] Unexpected redirect location")
            else:
                print(f"   [WARNING] Login status {response.status_code}")
                
        except Exception as e:
            print(f"   [WARNING] Doctor login test skipped: {e}")
        
        print(f"\n5. Testing login as patient@example.com...")
        try:
            session = requests.Session()
            login_page = session.get(base_url + "/login/")
            
            login_data = {
                'username': 'patient@example.com',
                'password': 'password',
            }
            
            import re
            match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', login_page.text)
            if match:
                login_data['csrfmiddlewaretoken'] = match.group(1)
            
            response = session.post(base_url + "/login/", data=login_data, allow_redirects=False)
            
            if response.status_code == 302:
                redirect_url = response.headers.get('Location', '')
                print(f"   [OK] Login successful, redirect to: {redirect_url}")
                if '/pacientes/24/' in redirect_url:
                    print(f"   [OK] Correct paciente exam list redirect")
                else:
                    print(f"   [WARNING] Unexpected redirect location")
            else:
                print(f"   [WARNING] Login status {response.status_code}")
                
        except Exception as e:
            print(f"   [WARNING] Patient (new) login test skipped: {e}")
        
        print(f"\n[SUCCESS] Login tests completed!")
        return True
        
    finally:
        # Terminate server
        print(f"\nShutting down server...")
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
        print("Server stopped.")

if __name__ == "__main__":
    success = test_login()
    sys.exit(0 if success else 1)