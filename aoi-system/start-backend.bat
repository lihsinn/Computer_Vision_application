@echo off
echo ========================================
echo Starting AOI Backend Server
echo ========================================
echo.

cd backend

if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Starting Flask server on http://localhost:5000
echo.
python run.py

pause
