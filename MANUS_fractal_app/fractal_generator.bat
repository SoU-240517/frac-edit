@echo off
cd /d "%~dp0"
echo フラクタルジェネレータを起動中...
python "%~dp0bin\fractal_generator.py"
if errorlevel 1 pause