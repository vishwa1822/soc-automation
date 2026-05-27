@echo off
cd /d "%~dp0"
echo Running full bootstrap + SOC API + dashboard...
call npm run go
pause
