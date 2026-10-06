@echo off
echo Building wheel file for scaffold
python -m build --wheel --outdir whl
if errorlevel 1 (
    echo Build failed
    exit /b 1
)
if exist scaffold.egg-info rmdir /s /q scaffold.egg-info
if exist build rmdir /s /q build
echo Build succeeded
