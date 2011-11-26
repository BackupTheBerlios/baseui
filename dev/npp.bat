@echo off
cd %1 
C:\Python26\python.exe %2

REM This makes notepad++ work together with python. Let npp execute that command:
REM "npp.bat" "$(CURRENT_DIRECTORY)" "$(FILE_NAME)"

echo.
pause
