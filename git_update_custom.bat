@echo off
cd /d D:\srcs

echo.
echo ============================
echo   PUSH TO GITHUB - CUSTOM
echo ============================
echo.

set /p commitmsg=Masukkan pesan commit: 

git add .
git commit -m "%commitmsg%"
git push origin main

echo.
echo ===== PUSH SELESAI =====
pause
