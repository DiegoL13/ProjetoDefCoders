@echo off
echo Starting Portal Saúde Development Server...
echo.
echo This will start the Django development server on http://127.0.0.1:8000
echo Press Ctrl+C to stop the server
echo.

cd /d "%~dp0"

echo Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python not found in PATH
    pause
    exit /b 1
)

echo.
echo Installing dependencies if needed...
pip install -r requirements.txt

echo.
echo Running database migrations...
cd sistema
python manage.py migrate

echo.
echo Collecting static files...
python manage.py collectstatic --noinput || echo "Collectstatic failed, continuing..."

echo.
echo Starting development server...
echo ========================================
echo   Portal Saúde Server Starting...
echo   URL: http://127.0.0.1:8000
echo   Admin: http://127.0.0.1:8000/admin/
echo ========================================
echo.

python manage.py runserver 127.0.0.1:8000

pause