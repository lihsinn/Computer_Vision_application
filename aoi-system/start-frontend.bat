@echo off
echo ========================================
echo Starting AOI Frontend Server
echo ========================================
echo.

cd frontend

if not exist node_modules (
    echo Installing dependencies...
    call npm install
    if errorlevel 1 (
        echo npm install failed, exiting.
        pause
        exit /b
    )
)


echo.
echo Starting Vite dev server...
echo Frontend will be available at http://localhost:5173
echo.
call npx vite

pause
