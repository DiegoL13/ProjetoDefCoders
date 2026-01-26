#!/usr/bin/env python
import os
import sys
import django

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'sistema'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema.settings')

django.setup()

from django.urls import reverse, NoReverseMatch

def test_url_reverses():
    print("Testing URL reverses...")
    
    # Test paciente-exames-list (should work)
    try:
        url = reverse('paciente-exames-list', kwargs={'paciente_id': 1})
        print(f"[OK] paciente-exames-list works: {url}")
    except NoReverseMatch as e:
        print(f"[FAIL] paciente-exames-list failed: {e}")
    
    # Test paciente-exames (should fail)
    try:
        url = reverse('paciente-exames', kwargs={'paciente_id': 1})
        print(f"[OK] paciente-exames works: {url}")
    except NoReverseMatch as e:
        print(f"[FAIL] paciente-exames failed (expected): {e}")
    
    # Test medico-dashboard (should work)
    try:
        url = reverse('medico-dashboard', kwargs={'medico_id': 1})
        print(f"[OK] medico-dashboard works: {url}")
    except NoReverseMatch as e:
        print(f"[FAIL] medico-dashboard failed: {e}")
    
    # Test medico-exames-list (should work if router generates it)
    try:
        url = reverse('medico-exames-list', kwargs={'medico_id': 1})
        print(f"[OK] medico-exames-list works: {url}")
    except NoReverseMatch as e:
        print(f"[FAIL] medico-exames-list failed: {e}")
    
    # Test medico-exames (should fail)
    try:
        url = reverse('medico-exames', kwargs={'medico_id': 1})
        print(f"[OK] medico-exames works: {url}")
    except NoReverseMatch as e:
        print(f"[FAIL] medico-exames failed (expected): {e}")
    
    # Test all router-generated URLs
    print("\nTesting all router-generated URLs:")
    from sistema.core.urls import router
    for prefix, viewset, basename in router.registry:
        print(f"\nBasename: {basename}")
        try:
            url = reverse(f'{basename}-list', kwargs={})
            print(f"  -list: {url}")
        except NoReverseMatch:
            print(f"  -list: NoReverseMatch")
        try:
            url = reverse(f'{basename}-detail', kwargs={'pk': 1})
            print(f"  -detail: {url}")
        except NoReverseMatch:
            print(f"  -detail: NoReverseMatch")

if __name__ == '__main__':
    test_url_reverses()