@echo off
cd /d "%~dp0.."

echo exit| python src\main.py ^
    --vfs .\vfs_examples\nested