#!/usr/bin/env python3
"""
Check production readiness for Portal Saúde.
Run: python check_production.py
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema.settings')
django.setup()

from django.conf import settings

def check_security():
    """Check security settings."""
    print("[SECURITY] Security Checks:")
    
    # Debug mode
    if settings.DEBUG:
        print("  [ERROR] DEBUG = True (should be False in production)")
    else:
        print("  [OK] DEBUG = False")
    
    # Allowed hosts
    if not settings.ALLOWED_HOSTS:
        print("  [ERROR] ALLOWED_HOSTS is empty")
    else:
        print(f"  [OK] ALLOWED_HOSTS = {settings.ALLOWED_HOSTS}")
    
    # Secret key
    if settings.SECRET_KEY.startswith('django-insecure-'):
        print("  [WARN]  SECRET_KEY is the default insecure key")
    else:
        print("  [OK] SECRET_KEY is custom")
    
    # Security middleware
    security_headers = [
        'django.middleware.security.SecurityMiddleware',
        'whitenoise.middleware.WhiteNoiseMiddleware',
    ]
    for mw in security_headers:
        if mw in settings.MIDDLEWARE:
            print(f"  [OK] Middleware '{mw}' found")
        else:
            print(f"  [ERROR] Middleware '{mw}' not found")
    
    # HTTPS settings
    if settings.SECURE_SSL_REDIRECT:
        print("  [OK] SECURE_SSL_REDIRECT = True")
    else:
        print("  [WARN]  SECURE_SSL_REDIRECT = False (set True with HTTPS)")
    
    if settings.SESSION_COOKIE_SECURE:
        print("  [OK] SESSION_COOKIE_SECURE = True")
    else:
        print("  [WARN]  SESSION_COOKIE_SECURE = False (set True with HTTPS)")
    
    if settings.CSRF_COOKIE_SECURE:
        print("  [OK] CSRF_COOKIE_SECURE = True")
    else:
        print("  [WARN]  CSRF_COOKIE_SECURE = False (set True with HTTPS)")

def check_database():
    """Check database configuration."""
    print("\n[DATABASE] Database Checks:")
    
    db = settings.DATABASES['default']
    engine = db['ENGINE']
    
    if 'sqlite3' in engine:
        print("  [WARN]  Using SQLite (not recommended for production)")
    elif 'postgresql' in engine or 'postgis' in engine:
        print("  [OK] Using PostgreSQL (recommended for production)")
    else:
        print(f"  [INFO]  Using {engine}")
    
    # Check if using environment variable
    if 'DATABASE_URL' in os.environ:
        print("  [OK] DATABASE_URL environment variable is set")
    else:
        print("  [INFO]  DATABASE_URL environment variable not set")

def check_static_files():
    """Check static files configuration."""
    print("\n[STATIC] Static Files Checks:")
    
    if hasattr(settings, 'STATIC_ROOT') and settings.STATIC_ROOT:
        print(f"  [OK] STATIC_ROOT = {settings.STATIC_ROOT}")
    else:
        print("  [ERROR] STATIC_ROOT not set")
    
    if hasattr(settings, 'STATICFILES_STORAGE'):
        storage = settings.STATICFILES_STORAGE
        if 'whitenoise' in storage:
            print(f"  [OK] Using WhiteNoise for static files: {storage}")
        else:
            print(f"  [INFO]  Static files storage: {storage}")
    else:
        print("  [ERROR] STATICFILES_STORAGE not set")
    
    # Check if static files directory exists
    if os.path.exists(settings.STATIC_ROOT):
        print(f"  [OK] Static files directory exists: {settings.STATIC_ROOT}")
    else:
        print(f"  [WARN]  Static files directory doesn't exist: {settings.STATIC_ROOT}")

def check_installed_apps():
    """Check installed apps for production."""
    print("\n[APPS] Installed Apps Checks:")
    
    required_apps = [
        'django.contrib.staticfiles',
        'rest_framework',
        'core',
    ]
    
    for app in required_apps:
        if app in settings.INSTALLED_APPS:
            print(f"  [OK] App '{app}' installed")
        else:
            print(f"  [ERROR] App '{app}' not installed")

def check_environment():
    """Check environment variables."""
    print("\n[ENV] Environment Checks:")
    
    # Check .env file
    env_file = os.path.join(settings.BASE_DIR.parent, '.env')
    if os.path.exists(env_file):
        print(f"  [OK] .env file found: {env_file}")
    else:
        print(f"  [WARN]  .env file not found: {env_file}")
    
    # Check critical environment variables
    critical_vars = ['SECRET_KEY', 'ALLOWED_HOSTS', 'DEBUG']
    for var in critical_vars:
        if var in os.environ:
            print(f"  [OK] Environment variable '{var}' is set")
        else:
            print(f"  [INFO]  Environment variable '{var}' not set (using default)")

def main():
    print("[START] Portal Saúde Production Readiness Check")
    print("=" * 50)
    
    try:
        check_security()
        check_database()
        check_static_files()
        check_installed_apps()
        check_environment()
        
        print("\n" + "=" * 50)
        print("[OK] Check completed!")
        print("\n[LIST] Next steps for production deployment:")
        print("1. Set DEBUG=False in .env file")
        print("2. Generate a new SECRET_KEY")
        print("3. Configure ALLOWED_HOSTS with your domain")
        print("4. Set up PostgreSQL database")
        print("5. Configure HTTPS (SSL/TLS certificates)")
        print("6. Set CSRF_COOKIE_SECURE=True and SESSION_COOKIE_SECURE=True")
        print("7. Run: python manage.py collectstatic --noinput")
        print("8. Deploy with Gunicorn + Nginx (see DEPLOY.md)")
        
        return 0
        
    except Exception as e:
        print(f"\n[ERROR] Error during checks: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())