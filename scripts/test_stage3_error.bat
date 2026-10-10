@echo off
cd /d "%~dp0.."

echo exit| python src\main.py ^
    --vfs .\vfs_examples\nested ^
    --script .\start_stage3_error.txt