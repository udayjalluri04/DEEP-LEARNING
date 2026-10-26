@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    py -3.12 -m venv .venv
    if errorlevel 1 (
        echo Could not create the virtual environment. Install Python 3.12 and try again.
        pause
        exit /b 1
    )
)

".venv\Scripts\python.exe" -c "import pandas, PIL, streamlit, ultralytics" >nul 2>nul
if errorlevel 1 (
    ".venv\Scripts\python.exe" -m pip install -r requirements.txt
    if errorlevel 1 (
        echo Could not install the application packages. Check the error above.
        pause
        exit /b 1
    )
)

start "" /B ".venv\Scripts\python.exe" -m streamlit run app.py --server.address 127.0.0.1 --server.headless true --browser.gatherUsageStats false
timeout /t 4 /nobreak >nul
start "" http://127.0.0.1:8501
echo The app is running at http://127.0.0.1:8501. Press Ctrl+C to stop it.
pause
