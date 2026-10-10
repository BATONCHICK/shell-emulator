@echo off
cd /d "%~dp0.."

python src\main.py ^
    --vfs .\vfs_examples\nested ^
    --script .\start_stage3.txt