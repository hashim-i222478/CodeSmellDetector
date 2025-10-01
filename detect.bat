@echo off
REM Code Smell Detector Shortcut Script
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%src"
C:/Users/hashi/AppData/Local/Programs/Python/Python313/python.exe detector_cli.py %*