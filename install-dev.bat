@echo off
echo Installing scaffold in development mode ...
.\.venv\Scripts\python.exe -m pip install -e .
echo Done! The package is now installed in editable mode.
pause 
