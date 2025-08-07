@echo off
cd /d D:\srcs

echo.
echo ========================
echo  AUTO PUSH TO GITHUB
echo ========================
echo.

git add .
git commit -m "Update SRCS - %date% %time%"
git push origin main

echo.
echo ===== DONE =====
pause
