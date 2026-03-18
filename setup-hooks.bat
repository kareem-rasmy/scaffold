@echo off

REM Setup script for team members to install shared Git hooks (Windows version)

echo Setting up Git hooks for this repository ...

REM COnfigure Git to use the shared hooks directory
git config core.hooksPath .githooks

echo.
echo Git hooks configured successfully!
echo The post-commit hook will now automatically update version.txt
echo.

pause
