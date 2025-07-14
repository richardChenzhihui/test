@echo off
cd /d %~dp0
echo [INFO] Installing dependencies...
npm install
echo [INFO] Starting backend...
npm start
pause