@echo off
REM Code Smell Detector GUI Launcher
echo Starting Code Smell Detector GUI...
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%src"
C:/Users/hashi/AppData/Local/Programs/Python/Python313/python.exe detector_gui.py
pause