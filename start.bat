@echo off
title AutoDeploy IT Portal - Server
cd /d "%~dp0"
echo ===================================================
echo     AutoDeploy IT - Zero-Touch Provisioning Portal
echo ===================================================
echo Memulai server portal di http://192.168.1.13:8000 ...
echo Tekan Ctrl+C untuk menghentikan server.
echo.
"C:\Users\Chaerul\AppData\Local\Programs\Python\Python310\python.exe" -m uvicorn app:app --host 0.0.0.0 --port 8000
pause
