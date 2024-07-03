@echo off

start winvnc.exe -run
timeout /t 1 >nul
start winvnc -connect 192.168.1.192::4444