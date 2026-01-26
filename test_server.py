#!/usr/bin/env python
import subprocess
import time
import sys
import os
import requests

def main():
    # Change to sistema directory
    os.chdir('sistema')
    
    # Start server
    print("Starting Django development server...")
    server = subprocess.Popen(
        [sys.executable, 'manage.py', 'runserver', '127.0.0.1:8000', '--noreload'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Give server time to start
    print("Waiting for server to start...")
    time.sleep(8)
    
    # Test endpoints
    base_url = 'http://127.0.0.1:8000'
    endpoints = [
        '/',
        '/cadastro/medico/',
        '/cadastro/paciente/',
        '/login/',
    ]
    
    for endpoint in endpoints:
        url = base_url + endpoint
        try:
            response = requests.get(url, timeout=5)
            print(f'[OK] {endpoint} - HTTP {response.status_code}')
        except Exception as e:
            print(f'[ERROR] {endpoint} - ERROR: {e}')
    
    # Kill server
    print("Stopping server...")
    server.terminate()
    server.wait()
    print("Server stopped.")
    
if __name__ == '__main__':
    main()