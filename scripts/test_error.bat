@echo off
cd /d "%~dp0.."
echo exit| python src\main.py --vfs .\test_vfs --script .\start_error.txt