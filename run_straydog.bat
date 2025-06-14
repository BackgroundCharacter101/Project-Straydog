@echo off
:: Elevate admin if not already
openfiles >nul 2>&1
if %errorlevel% neq 0 (
    powershell -Command "Start-Process '%~f0' -Verb runAs"
    exit /b
)

start "" /b "%~dp0client.exe"
