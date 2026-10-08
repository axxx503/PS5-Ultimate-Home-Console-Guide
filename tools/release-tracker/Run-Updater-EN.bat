@echo off
cd /d "%~dp0"
where py >nul 2>&1
if %errorlevel%==0 (py -3 updater.py --lang en) else (python updater.py --lang en)
pause
